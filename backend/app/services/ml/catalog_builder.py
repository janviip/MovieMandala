from __future__ import annotations

from pathlib import Path
from typing import Iterable, Any

import pandas as pd
from tqdm import tqdm

from ...domain.movie_features import MovieFeatureRecord
from .tmdb_client import TMDBClient


def _safe_name_list(items: Iterable[dict[str, Any]], key: str = "name") -> tuple[str, ...]:
    values: list[str] = []
    for item in items or []:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
    return tuple(dict.fromkeys(values))


def _extract_directors(crew: Iterable[dict[str, Any]]) -> tuple[str, ...]:
    directors: list[str] = []
    for person in crew or []:
        if person.get("job") == "Director" and person.get("name"):
            directors.append(str(person["name"]).strip())
    return tuple(dict.fromkeys(directors))


def tmdb_details_to_feature_record(payload: dict[str, Any], top_cast_n: int = 8) -> MovieFeatureRecord:
    """
    Convert one enriched TMDB movie payload into the ML-facing feature record.
    """

    credits = payload.get("credits") or {}
    keywords_payload = payload.get("keywords") or {}

    # TMDB can return keywords differently for movies vs TV. For movies, it is usually {"keywords": [...]}
    keywords = keywords_payload.get("keywords") or keywords_payload.get("results") or []

    cast_items = credits.get("cast") or []
    cast_items = sorted(cast_items, key=lambda x: x.get("order", 10_000))[:top_cast_n]

    return MovieFeatureRecord(
        tmdb_id=int(payload["id"]),
        title=str(payload.get("title") or payload.get("original_title") or "").strip(),
        overview=str(payload.get("overview") or "").strip(),
        release_date=str(payload.get("release_date") or "").strip(),
        popularity=float(payload.get("popularity") or 0.0),
        vote_average=float(payload.get("vote_average") or 0.0),
        vote_count=int(payload.get("vote_count") or 0),
        genres=_safe_name_list(payload.get("genres") or []),
        keywords=_safe_name_list(keywords),
        cast=_safe_name_list(cast_items),
        directors=_extract_directors(credits.get("crew") or []),
        poster_path=payload.get("poster_path"),
    )


class TMDBCatalogBuilder:
    """
    Builds a movie catalog for offline ML artifact creation.

    This class should usually be called from a script or notebook, not from
    a request-response API route. Catalog creation makes many external calls.
    """

    def __init__(self, client: TMDBClient | None = None) -> None:
        self.client = client or TMDBClient()

    def collect_movie_ids(self, pages: int = 25) -> list[int]:
        ids: list[int] = []
        for page in tqdm(range(1, pages + 1), desc="Discovering TMDB movie IDs"):
            payload = self.client.discover_movies(page=page)
            for row in payload.get("results", []):
                movie_id = row.get("id")
                if movie_id is not None:
                    ids.append(int(movie_id))
        return list(dict.fromkeys(ids))

    def build_catalog(self, pages: int = 25, top_cast_n: int = 8) -> pd.DataFrame:
        movie_ids = self.collect_movie_ids(pages=pages)

        records: list[dict[str, Any]] = []
        failed: list[int] = []

        for tmdb_id in tqdm(movie_ids, desc="Fetching enriched movie details"):
            try:
                details = self.client.movie_details(tmdb_id)
                record = tmdb_details_to_feature_record(details, top_cast_n=top_cast_n)
                if record.title and record.overview:
                    records.append(record.to_dict())
            except Exception:
                failed.append(tmdb_id)

        df = pd.DataFrame(records)
        if df.empty:
            raise RuntimeError("No movies collected from TMDB.")

        df = df.drop_duplicates(subset=["tmdb_id"]).reset_index(drop=True)
        df["genres"] = df["genres"].apply(tuple)
        df["keywords"] = df["keywords"].apply(tuple)
        df["cast"] = df["cast"].apply(tuple)
        df["directors"] = df["directors"].apply(tuple)

        if failed:
            print(f"Skipped {len(failed)} movies due to TMDB fetch/parse errors.")

        return df

    @staticmethod
    def save_catalog(df: pd.DataFrame, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix.lower() == ".parquet":
            df.to_parquet(path, index=False)
        elif path.suffix.lower() in {".jsonl", ".json"}:
            df.to_json(path, orient="records", lines=path.suffix.lower() == ".jsonl")
        else:
            df.to_csv(path, index=False)
