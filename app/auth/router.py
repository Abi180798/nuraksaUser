""" AUTH ROUTER.

Define all auth endpoint here like login, refresh token ec

"""

from fastapi import APIRouter

from .views import *
from app.response import *


auth_router = APIRouter()
auth_views = AuthViews()

@auth_router.post("/login", status_code = status.HTTP_201_CREATED, response_model = AuthResponse)
def login(
    res : Response,
    login_data : OAuth2PasswordRequestForm = Depends()
    ):
    return httpResponse(
        auth_views.post,
        res = res,
        login_data = login_data
    )
@auth_router.get("/authorized", status_code = status.HTTP_201_CREATED)
def getToken(
    res : Response,
    current_user : UserModel = Depends(auth_views.get_current_active_user),
    ):
    response = BaseResponse()
    response.notfound()
    res.status_code = response.status_code
    if current_user is not None:
        response.status_code = status.HTTP_200_OK
        response.filed = False
        response.message = "Token is authorized"
        res.status_code = response.status_code
    return response