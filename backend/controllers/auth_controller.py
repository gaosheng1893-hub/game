from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserRegister, Token
from services.auth_service import AuthService
from common.jwt_utils import get_current_user

router = APIRouter()

@router.post("/register")
async def register(user: UserRegister):
    return AuthService.register_user(user.username, user.email, user.password)

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return AuthService.login_user(form_data.username, form_data.password)

@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
