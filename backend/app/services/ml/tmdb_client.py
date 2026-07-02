from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import httpx


class TMDBClientError(RuntimeError):
    """Raised when TMDB returns an error response."""


@dataclass(frozen=True)
class TMDBClientConfig:
    api_key: str | None = None
    read_token: str | None = None
    base_url: str = "https://api.themoviedb.org/3"
    timeout_seconds: float = 20.0
    request_sleep_seconds: float = 0.25

    @classmethod
    def from_env(cls) -> "TMDBClientConfig":
        return cls(
            api_key=os.getenv("TMDB_API_KEY"),
            read_token=os.getenv("TMDB_API_READ_TOKEN"),
        )


class TMDBClient:
    """
    Minimal TMDB client for ML catalog creation.

    Supports either:
    - TMDB_API_KEY as v3 query parameter
    - TMDB_API_READ_TOKEN as v4 Bearer token
    """

    def __init__(self, config: TMDBClientConfig | None = None) -> None:
        self.config = config or TMDBClientConfig.from_env()
        if not self.config.api_key and not self.config.read_token:
            raise ValueError(
                "TMDB credentials missing. Set TMDB_API_KEY or TMDB_API_READ_TOKEN."
            )

    def _headers(self) -> dict[str, str]:
        if self.config.read_token:
            return {
                "Authorization": f"Bearer {self.config.read_token}",
                "accept": "application/json",
            }
        return {"accept": "application/json"}

    def _params(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        merged = dict(params or {})
        if self.config.api_key:
            merged["api_key"] = self.config.api_key
        return merged

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        time.sleep(self.config.request_sleep_seconds)

        with httpx.Client(timeout=self.config.timeout_seconds) as client:
            response = client.get(url, headers=self._headers(), params=self._params(params))

        if response.status_code >= 400:
            raise TMDBClientError(
                f"TMDB request failed: {response.status_code} {response.text[:500]}"
            )
        return response.json()

    def discover_movies(
        self,
        page: int,
        sort_by: str = "popularity.desc",
        language: str = "en-US",
        include_adult: bool = False,
        vote_count_gte: int = 20,
    ) -> dict[str, Any]:
        return self.get(
            "/discover/movie",
            {
                "page": page,
                "sort_by": sort_by,
                "language": language,
                "include_adult": str(include_adult).lower(),
                "vote_count.gte": vote_count_gte,
            },
        )

    def movie_details(self, tmdb_id: int, language: str = "en-US") -> dict[str, Any]:
        return self.get(
            f"/movie/{tmdb_id}",
            {
                "language": language,
                "append_to_response": "credits,keywords",
            },
        )
