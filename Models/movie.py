from pydantic import BaseModel ,Field
from typing import Optional

class Movie(BaseModel):
    id:Optional[int] = None
    title:str = Field(dmin_length=3, max_length=50)
    overview:str = Field(min_length=15, max_length=50)
    category:str =  Field(min_length=3, max_length=50)
    raiting:float = Field(gt=1,le=10)
    year :int =Field(gt=1880,le=2023)
    
  
    class Config:
        extra = "forbid"
    schema_extra = {
        "example": {
            "title": "mi pelicula",
            "overview": "esta es la reseña de mi pelicula",
            "year": 2022,
            "rating": 1,
            "category": "esta es la reseña de mi pelicula"
        }
    }

#class MovieWithId(Movie):
#    id:int