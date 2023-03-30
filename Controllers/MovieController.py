from movies import movies
from Entities.movie import Movie
from fastapi import Path, Query,APIRouter,Depends
from typing import List
from fastapi.responses import HTMLResponse, JSONResponse
from Controllers.UserController import JWTBearer
from Models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from Config.database import Session

db = Session()
router = APIRouter()
def updateMovie(movie: Movie, movie_to_update: dict):
    movie_to_update['title'] = movie.title
    movie_to_update['year'] = movie.year
    movie_to_update['raiting'] = movie.raiting
    movie_to_update['overview'] = movie.overview
    movie_to_update['category'] = movie.category

class Movierouter:
    @router.get("/",tags=['home'])
    def read_root():
        #podemos retornar tanto diccionarios como codigo html
        #return {"response:"HelloWord""}
        return HTMLResponse('<h1>World</h1>')
    

    @router.get('/movies',tags=['movies'],response_model=List[Movie])
    def get_movies()->List[Movie]:
        return JSONResponse(content=jsonable_encoder(db.query(MovieModel).all()))


    @router.get('/movies/{id}',tags=['movies'],response_model=Movie,status_code=200)
    async def get_movie_by_id(id:int = Path(ge=1,le=2023))->Movie:
        try:
            return JSONResponse(status_code=200,content =jsonable_encoder(db.query(MovieModel).filter(MovieModel.id == id)))
        except IndexError:
            return{"error":"Pelicula no encontrada"}
        #try:
        #    return [ movie for movie in movies if movie['id'] == id][0]
        #except IndexError:
        #    return {"error": "Movie not found"}

    #para utilizar queryparameter en una url que ya existe le agregamos una barra al final
    @router.get('/movies/',tags=['movies'])
    def get_movies_by_category(category: str = Query(min_length=15,max_length=50)):
        movie = next(filter(lambda x: x['category'] == category,movies),None)
        return movie or {"error":"No se encontro la pelicula"}

    @router.post('/movies',tags=['movies'])
    async def create_movie(movie: Movie):
        new_movie = MovieModel(**movie.dict())
        new_movie.id = max(db.query(MovieModel).all(), key=lambda x: x.id).id + 1
        db.add(new_movie)
        db.commit()
        movies.append(movie.dict())
        return {"movie": movie}

   

    @router.put('/movies/{id}',tags=['movies'])
    async def update_movie(id: int, movie: Movie):
        movie_to_update = next(filter(lambda x: x['id'] == id, movies), None)
        if not movie_to_update:
            return {"status_code":"404","detail":"Movie not found"}
        updateMovie(movie, movie_to_update)
        return movie_to_update
    # else: return{"error":"No se pudo actualizar la pelicula"}
    
    @router.delete('/movies/{id}',tags=['movies'],dependencies=[Depends(JWTBearer())])
    async def delete_movie(id:int):
        movie_to_delete = next(filter(lambda x: x['id'] == id, movies), None)
        if movie_to_delete != None:
            movies.remove(movie_to_delete)
        return movies