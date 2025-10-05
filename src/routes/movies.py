from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/")
async def get_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
) -> MovieListResponseSchema:
    total_items_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_items_result.scalar_one()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    prev_page = None
    if page > 1:
        prev_page = f"/api/v1/theater/movies/?page={page - 1}&per_page={per_page}"

    next_page = None
    if page < total_pages:
        next_page = f"/api/v1/theater/movies/?page={page + 1}&per_page={per_page}"

    movies_list = [
        MovieDetailResponseSchema(
            id=movie.id,
            name=movie.name,
            date=str(movie.date),
            score=movie.score,
            genre=movie.genre,
            overview=movie.overview,
            crew=movie.crew,
            orig_title=movie.orig_title,
            status=movie.status,
            orig_lang=movie.orig_lang,
            budget=float(movie.budget),
            revenue=movie.revenue,
            country=movie.country,
        )
        for movie in movies
    ]

    return MovieListResponseSchema(
        movies=movies_list,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movie_id}/")
async def get_movie_by_id(
    movie_id: int, db: AsyncSession = Depends(get_db)
) -> MovieDetailResponseSchema:
    movie: MovieModel | None = await db.get(MovieModel, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return MovieDetailResponseSchema(
        id=movie.id,
        name=movie.name,
        date=str(movie.date),
        score=movie.score,
        genre=movie.genre,
        overview=movie.overview,
        crew=movie.crew,
        orig_title=movie.orig_title,
        status=movie.status,
        orig_lang=movie.orig_lang,
        budget=float(movie.budget),
        revenue=movie.revenue,
        country=movie.country,
    )
