from movies import movies
from Entities.movie import Movie
from fastapi import Path, Query,APIRouter,Depends
from typing import List
from fastapi.responses import HTMLResponse, JSONResponse
from midleware.jwt_bearer import JWTBearer
from Models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from Config.database import Session
from services.movie_service import MovieService

db = Session()
router = APIRouter()
def updateMovie(movie: Movie, movie_to_update: MovieModel):
    movie_to_update.title = movie.title
    movie_to_update.year = movie.year
    movie_to_update.raiting = movie.raiting
    movie_to_update.overview = movie.overview
    movie_to_update.category = movie.category

class Movierouter:
    @router.get("/",tags=['home'])
    def read_root():
        #podemos retornar tanto diccionarios como codigo html
        #return {"response:"HelloWord""}
        return HTMLResponse('<h1>World</h1>')
    

    @router.get('/movies',response_model=List[Movie])
    def get_movies()->List[Movie]:
        return JSONResponse(content=jsonable_encoder(MovieService(db).get_movies()))


    @router.get('/movies/{id}',tags=['movies'],response_model=Movie,status_code=200)
    async def get_movie_by_id(id:int = Path(ge=1,le=2023))->Movie:
        try:
            return JSONResponse(status_code=200,content =jsonable_encoder(MovieService(db).get_movie_by_id(id)))
        except IndexError:
            return{"error":"Pelicula no encontrada"}
        #try:
        #    return [ movie for movie in movies if movie['id'] == id][0]
        #except IndexError:
        #    return {"error": "Movie not found"}


    #para utilizar queryparameter en una url que ya existe le agregamos una barra al final
    @router.get('/movies/',tags=['movies'])
    def get_movies_by_category(category: str = Query(min_length=3,max_length=50)):
        return JSONResponse (status_code=200,content=jsonable_encoder(MovieService(db).get_movies_by_category(category))) or JSONResponse(status_code=404,content={"error":"No se encontro la pelicula"})
         


    @router.post('/movies',tags=['movies'])
    async def create_movie(movie: Movie):
        return JSONResponse(status_code=201,content={"Message":"Pelicula agregada correctamente"}) if MovieService(db).create_movie(movie) else  JSONResponse(status_code=201,content={"error":"Error al agregar la pelicula"})
          

    @router.put('/movies/{id}',tags=['movies'])
    async def update_movie(id: int, movie: Movie):
        movie_to_update = MovieService(db).get_movie_by_id(id)
        if not movie_to_update:
            return {"status_code":"404","detail":"Movie not found"}
       
        MovieService(db).update_movie(movie_to_update,movie)
        return JSONResponse(status_code=202,content={"Message":"Pelicula Modificada Exitosamente"}) 
    # else: return{"error":"No se pudo actualizar la pelicula"}
    
    @router.delete('/movies/{id}',tags=['movies'],dependencies=[Depends(JWTBearer())])
    async def delete_movie(id:int):
        movie_to_delete = MovieService(db).get_movie_by_id(id)
        if  movie_to_delete != None:            
            MovieService(db).delete_movie(movie_to_delete)
            return JSONResponse(status_code=203,content= {"Message":"Pelicula eliminada exitosamente"})
        
        return JSONResponse(status_code=205,content={"Message":"La pelicula no existe"})    
    
    
    
    