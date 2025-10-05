from pydantic import BaseModel
from typing import Optional


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: str
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
