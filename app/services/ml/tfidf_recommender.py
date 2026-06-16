from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Any

import joblib
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.ml.preprocessing import MovieFeaturePreprocessor, normalize_text


SearchMode = Literal["title", "tmdb_id", "free_text"]


def _as_str_tuple(value: Any) -> tuple[str, ...]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ()
    if isinstance(value, np.ndarray):
        value = value.tolist()
    elif not isinstance(value, (list, tuple)):
        value = [value]
    return tuple(str(item) for item in value if item is not None and not pd.isna(item))


def _optional_str(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return str(value)


@dataclass(frozen=True)
class RecommendationResult:
    tmdb_id: int
    title: str
    score: float
    overview: str
    release_date: str = ""
    genres: tuple[str, ...] = ()
    poster_path: str | None = None
    vote_average: float = 0.0
    popularity: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "tmdb_id": self.tmdb_id,
            "title": self.title,
            "score": self.score,
            "overview": self.overview,
            "release_date": self.release_date,
            "genres": self.genres,
            "poster_path": self.poster_path,
            "vote_average": self.vote_average,
            "popularity": self.popularity,
        }


class MovieRecommender:
    """
    TF-IDF + cosine-similarity movie recommender.

    Fit offline:
        recommender = MovieRecommender()
        recommender.fit(catalog_df)
        recommender.save("artifacts")

    Load in FastAPI:
        recommender = MovieRecommender.load("artifacts")
        recommender.recommend("Inception", k=10)
    """

    def __init__(
        self,
        vectorizer: TfidfVectorizer | None = None,
        preprocessor: MovieFeaturePreprocessor | None = None,
    ) -> None:
        self.vectorizer = vectorizer or TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.90,
            max_features=50_000,
            sublinear_tf=True,
            norm="l2",
        )
        self.preprocessor = preprocessor or MovieFeaturePreprocessor()
        self.catalog_: pd.DataFrame | None = None
        self.matrix_: sparse.csr_matrix | None = None
        self.tmdb_id_to_index_: dict[int, int] = {}
        self.title_to_indices_: dict[str, list[int]] = {}

    def fit(self, catalog: pd.DataFrame) -> "MovieRecommender":
        processed = self.preprocessor.transform(catalog)
        matrix = self.vectorizer.fit_transform(processed["feature_text"])

        self.catalog_ = processed.reset_index(drop=True)
        self.matrix_ = matrix.tocsr()
        self.tmdb_id_to_index_ = {
            int(tmdb_id): int(i)
            for i, tmdb_id in enumerate(self.catalog_["tmdb_id"].tolist())
        }
        self.title_to_indices_ = self._build_title_index(self.catalog_)

        return self

    def _require_fitted(self) -> None:
        if self.catalog_ is None or self.matrix_ is None:
            raise RuntimeError("MovieRecommender is not fitted. Call fit(...) or load(...).")

    @staticmethod
    def _build_title_index(catalog: pd.DataFrame) -> dict[str, list[int]]:
        title_to_indices: dict[str, list[int]] = {}
        for idx, title in enumerate(catalog["title"].astype(str).tolist()):
            key = normalize_text(title).lower()
            title_to_indices.setdefault(key, []).append(idx)
        return title_to_indices

    def _resolve_title_index(self, title: str) -> int:
        self._require_fitted()
        assert self.catalog_ is not None

        normalized = normalize_text(title).lower()
        exact = self.title_to_indices_.get(normalized)
        if exact:
            return exact[0]

        # Simple fallback: choose title with highest character-level containment.
        titles = self.catalog_["title"].astype(str).str.lower()
        contains = self.catalog_[titles.str.contains(normalized, regex=False, na=False)]
        if not contains.empty:
            return int(contains.index[0])

        raise ValueError(f"No movie title found for query: {title!r}")

    def _recommend_from_index(
        self,
        source_index: int,
        k: int = 10,
        exclude_self: bool = True,
    ) -> list[RecommendationResult]:
        self._require_fitted()
        assert self.catalog_ is not None
        assert self.matrix_ is not None

        if source_index < 0 or source_index >= self.matrix_.shape[0]:
            raise IndexError(f"source_index out of range: {source_index}")

        query_vector = self.matrix_[source_index]
        scores = cosine_similarity(query_vector, self.matrix_).ravel()

        if exclude_self:
            scores[source_index] = -np.inf

        # Efficient top-k without sorting the full catalog.
        k = max(1, min(k, len(scores) - int(exclude_self)))
        candidate_indices = np.argpartition(-scores, kth=k - 1)[:k]
        ranked_indices = candidate_indices[np.argsort(-scores[candidate_indices])]

        return [self._row_to_result(int(i), float(scores[i])) for i in ranked_indices]

    def recommend_by_tmdb_id(self, tmdb_id: int, k: int = 10) -> list[dict[str, Any]]:
        self._require_fitted()
        source_index = self.tmdb_id_to_index_.get(int(tmdb_id))
        if source_index is None:
            raise ValueError(f"TMDB id not found in recommender catalog: {tmdb_id}")
        return [result.to_dict() for result in self._recommend_from_index(source_index, k=k)]

    def recommend_by_title(self, title: str, k: int = 10) -> list[dict[str, Any]]:
        source_index = self._resolve_title_index(title)
        return [result.to_dict() for result in self._recommend_from_index(source_index, k=k)]

    def recommend_from_text(self, text: str, k: int = 10) -> list[dict[str, Any]]:
        """
        Recommend movies from arbitrary text, such as:
        'space exploration psychological thriller artificial intelligence'

        This does not require the query movie to exist in the catalog.
        """
        self._require_fitted()
        assert self.catalog_ is not None
        assert self.matrix_ is not None

        query = normalize_text(text)
        if len(query) < 3:
            raise ValueError("Free-text query is too short.")

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix_).ravel()

        k = max(1, min(k, len(scores)))
        candidate_indices = np.argpartition(-scores, kth=k - 1)[:k]
        ranked_indices = candidate_indices[np.argsort(-scores[candidate_indices])]

        return [self._row_to_result(int(i), float(scores[i])).to_dict() for i in ranked_indices]

    def recommend(
        self,
        query: str | int,
        k: int = 10,
        mode: SearchMode = "title",
    ) -> list[dict[str, Any]]:
        if mode == "title":
            return self.recommend_by_title(str(query), k=k)
        if mode == "tmdb_id":
            return self.recommend_by_tmdb_id(int(query), k=k)
        if mode == "free_text":
            return self.recommend_from_text(str(query), k=k)
        raise ValueError(f"Unsupported recommendation mode: {mode}")

    def _row_to_result(self, index: int, score: float) -> RecommendationResult:
        self._require_fitted()
        assert self.catalog_ is not None

        row = self.catalog_.iloc[index]

        return RecommendationResult(
            tmdb_id=int(row["tmdb_id"]),
            title=str(row["title"]),
            score=round(float(score), 6),
            overview=str(row.get("overview", "") or ""),
            release_date=str(row.get("release_date", "") or ""),
            genres=_as_str_tuple(row.get("genres")),
            poster_path=_optional_str(row.get("poster_path")),
            vote_average=float(row.get("vote_average", 0.0) or 0.0),
            popularity=float(row.get("popularity", 0.0) or 0.0),
        )

    def save(self, artifact_dir: str | Path) -> None:
        self._require_fitted()
        assert self.catalog_ is not None
        assert self.matrix_ is not None

        artifact_dir = Path(artifact_dir)
        artifact_dir.mkdir(parents=True, exist_ok=True)

        self.catalog_.to_parquet(artifact_dir / "movie_catalog.parquet", index=False)
        joblib.dump(self.vectorizer, artifact_dir / "tfidf_vectorizer.joblib")
        joblib.dump(self.matrix_, artifact_dir / "tfidf_matrix.joblib")
        joblib.dump(
            {
                "tmdb_id_to_index": self.tmdb_id_to_index_,
                "title_to_indices": self.title_to_indices_,
            },
            artifact_dir / "movie_index.joblib",
        )

    @classmethod
    def load(cls, artifact_dir: str | Path) -> "MovieRecommender":
        artifact_dir = Path(artifact_dir)

        catalog_path = artifact_dir / "movie_catalog.parquet"
        vectorizer_path = artifact_dir / "tfidf_vectorizer.joblib"
        matrix_path = artifact_dir / "tfidf_matrix.joblib"
        index_path = artifact_dir / "movie_index.joblib"

        missing = [
            str(path)
            for path in [catalog_path, vectorizer_path, matrix_path, index_path]
            if not path.exists()
        ]
        if missing:
            raise FileNotFoundError(f"Missing recommender artifacts: {missing}")

        recommender = cls(vectorizer=joblib.load(vectorizer_path))
        recommender.catalog_ = pd.read_parquet(catalog_path)
        recommender.matrix_ = joblib.load(matrix_path).tocsr()

        index_payload = joblib.load(index_path)
        recommender.tmdb_id_to_index_ = {
            int(k): int(v)
            for k, v in index_payload["tmdb_id_to_index"].items()
        }
        recommender.title_to_indices_ = {
            str(k): [int(i) for i in v]
            for k, v in index_payload["title_to_indices"].items()
        }

        return recommender
