from fastapi import Header, Depends, FastAPI, Path, Query
from routes import router
app = FastAPI()
app.title = "Api de peliculas"
app.version = "1.0.0"

app.include_router(router,prefix="")


