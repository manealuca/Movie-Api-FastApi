from fastapi import Header, Depends, FastAPI, Path, Query
from routers.routes import router
from Config.database import Session,engine,Base
from midleware.error_handle import ErrorHandle
from midleware.jwt_bearer import JWTBearer
app = FastAPI()
app.title = "Api de peliculas"
app.version = "1.0.0"

app.add_middleware(ErrorHandle)
#app.add_middleware(JWTBearer)
Base.metadata.create_all(bind=engine)
app.include_router(router,prefix="")
