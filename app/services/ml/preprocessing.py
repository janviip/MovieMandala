from __future__ import annotations

import re
import unicodedata
from typing import Iterable, Any

import pandas as pd


_WHITESPACE_RE = re.compile(r"\s+")
_NON_ALNUM_KEEP_SPACE_RE = re.compile(r"[^a-zA-Z0-9_ ]+")


def normalize_text(text: Any) -> str:
    """
    Normalize free text while keeping enough semantic content for TF-IDF.

    TF-IDF already handles lowercasing and tokenization, so this function only
    removes noisy unicode/control artifacts and excessive whitespace.
    """

    if text is None:
        return ""

    text = str(text)
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\x00", " ")
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


def normalize_token(token: Any) -> str:
    """
    Normalize names/phrases into single tokens.

    Example:
    - "Science Fiction" -> "science_fiction"
    - "Tom Hanks" -> "tom_hanks"

    This helps TF-IDF preserve multiword entities.
    """

    token = normalize_text(token).lower()
    token = token.replace("&", " and ")
    token = _NON_ALNUM_KEEP_SPACE_RE.sub(" ", token)
    token = _WHITESPACE_RE.sub("_", token).strip("_")
    return token


def normalize_token_list(values: Any) -> list[str]:
    if values is None:
        return []

    if isinstance(values, str):
        # Handles CSV-like fallback if data came from CSV.
        raw_values = [v.strip() for v in values.split(",")]
    else:
        raw_values = list(values)

    cleaned: list[str] = []
    for value in raw_values:
        token = normalize_token(value)
        if token:
            cleaned.append(token)

    return list(dict.fromkeys(cleaned))


class MovieFeaturePreprocessor:
    """
    Creates the final text field used by TF-IDF.

    The weighting is intentionally simple and transparent:
    - overview is natural language and gets strong semantic weight
    - genres/keywords/cast/director are repeated to increase their influence
    - title is included, but not over-weighted
    """

    def __init__(
        self,
        overview_weight: int = 3,
        genre_weight: int = 3,
        keyword_weight: int = 3,
        cast_weight: int = 2,
        director_weight: int = 2,
        title_weight: int = 1,
    ) -> None:
        self.overview_weight = overview_weight
        self.genre_weight = genre_weight
        self.keyword_weight = keyword_weight
        self.cast_weight = cast_weight
        self.director_weight = director_weight
        self.title_weight = title_weight

    def build_feature_text_for_row(self, row: pd.Series) -> str:
        title = normalize_text(row.get("title", ""))
        overview = normalize_text(row.get("overview", ""))

        genres = normalize_token_list(row.get("genres", []))
        keywords = normalize_token_list(row.get("keywords", []))
        cast = normalize_token_list(row.get("cast", []))
        directors = normalize_token_list(row.get("directors", []))

        parts: list[str] = []
        parts.extend([title] * self.title_weight)
        parts.extend([overview] * self.overview_weight)
        parts.extend([" ".join(genres)] * self.genre_weight)
        parts.extend([" ".join(keywords)] * self.keyword_weight)
        parts.extend([" ".join(cast)] * self.cast_weight)
        parts.extend([" ".join(directors)] * self.director_weight)

        return normalize_text(" ".join(part for part in parts if part))

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        required = {"tmdb_id", "title", "overview"}
        missing = sorted(required.difference(df.columns))
        if missing:
            raise ValueError(f"Catalog is missing required columns: {missing}")

        out = df.copy()

        for col in ["genres", "keywords", "cast", "directors"]:
            if col not in out.columns:
                out[col] = [[] for _ in range(len(out))]

        out["feature_text"] = out.apply(self.build_feature_text_for_row, axis=1)

        # Remove records that cannot produce useful TF-IDF features.
        out = out[out["feature_text"].str.len() > 20].copy()
        out = out.drop_duplicates(subset=["tmdb_id"]).reset_index(drop=True)
        return out
