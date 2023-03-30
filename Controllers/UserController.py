from Models.User import User
from fastapi import Path, Query,APIRouter, Request, HTTPException
from fastapi.security import HTTPBearer
from typing import List
from fastapi.responses import HTMLResponse, JSONResponse
from jwtManager import creaate_token, validate_token
router = APIRouter()

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data= validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403,detail="Credenciales invalidas",)


@router.post('/login',tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = creaate_token(user.dict())
        return JSONResponse(status_code=200,content=token)