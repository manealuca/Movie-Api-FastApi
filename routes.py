from fastapi import APIRouter
from Controllers import UserController as user_controller
from Controllers import MovieController as movies
router  = APIRouter()
router.include_router(movies.router,prefix="/movies")
router.include_router(user_controller.router,prefix="/user")
