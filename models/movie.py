from pydantic import BaseModel

class Movie(BaseModel):
    rank: int
    movie_title: str
    year: int
    score: int
    director: str
    cast: str
    critics: str