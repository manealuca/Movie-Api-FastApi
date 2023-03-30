from fastapi import Header, Depends, FastAPI, Path, Query
from routes import router
from Config.database import Session,engine,Base
from Models.movie import Movie
app = FastAPI()
app.title = "Api de peliculas"
app.version = "1.0.0"
Base.metadata.create_all(bind=engine)
app.include_router(router,prefix="")


