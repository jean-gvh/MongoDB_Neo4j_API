from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class Movie(BaseModel):
    plot: str
    genres: List[str]
    runtime: int
    cast: List[str]
    poster: str
    title: str
    fullplot: str = ""  # Définir une valeur par défaut pour fullplot
    languages: List[str]
    released: datetime
    directors: List[str]
    rated: str
    awards: dict
    lastupdated: datetime
    year: int
    imdb: dict
    countries: List[str]
    type: str
    tomatoes: Optional[dict] = Field(default_factory=dict)
    num_mflix_comments: int = 0


    # QUESTION 3
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    plot: Optional[str] = None
    fullplot: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    runtime: Optional[int] = None
    rated: Optional[str] = None
    cast: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list) 
    countries: List[str] = Field(default_factory=list)
    directors: List[str] = Field(default_factory=list) 
    writers: List[str] = Field(default_factory=list)


class PersonMovieReview(BaseModel):
    name: str
    nbMovies: Optional[int]
    moviesRated: Optional[List[str]]





    