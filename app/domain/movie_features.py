from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class MovieFeatureRecord:
    """
    ML-facing movie representation.

    This is intentionally separate from SQLAlchemy models and API schemas.
    The recommender only needs stable feature fields, not auth, history,
    database sessions, or route-level concerns.
    """

    tmdb_id: int
    title: str
    overview: str = ""
    release_date: str = ""
    popularity: float = 0.0
    vote_average: float = 0.0
    vote_count: int = 0
    genres: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    cast: tuple[str, ...] = ()
    directors: tuple[str, ...] = ()
    poster_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def year(self) -> int | None:
        if not self.release_date:
            return None
        try:
            return int(self.release_date[:4])
        except ValueError:
            return None
