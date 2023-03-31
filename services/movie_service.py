from Models.movie import Movie as MovieModel
from Entities.movie import Movie
class MovieService():
    def __init__(self,db)->None:
        self.db = db
        
    def get_movies(self):
        return self.db.query(MovieModel).all()
    
    def get_movie_by_id(self, id:int):
        return self.db.query(MovieModel).filter(MovieModel.id == id).first()
    
    def get_movies_by_category(self,category:str):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()
    
    def new_id(self):
        return max(self.db.query(MovieModel).all(), key=lambda x: x.id).id + 1
    
    def create_movie(self, movie:Movie):
        try:
            new_movie = MovieModel(**movie.dict())
            new_movie.id = self.new_id()
            self.db.add(new_movie)
            self.db.commit()
            return True
        except:
            return False    
        
    def update_movie(self,movie_to_update:MovieModel,movie:Movie):
        try:
            movie_to_update.title = movie.title
            movie_to_update.year = movie.year
            movie_to_update.raiting = movie.raiting
            movie_to_update.overview = movie.overview
            movie_to_update.category = movie.category
            self.db.commit()
            return True
        except: return False
        
        
    def delete_movie(self,movie:MovieModel):
        try:
            self.db.delete(movie)
            self.db.commit()
            return True
        except: return False