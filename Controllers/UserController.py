from Entities.User import User
from fastapi import APIRouter

from typing import List
from fastapi.responses import JSONResponse
from jwtManager import creaate_token
router = APIRouter()

@router.post('/login',tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = creaate_token(user.dict())
        return JSONResponse(status_code=200,content=token)