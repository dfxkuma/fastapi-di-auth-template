from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, Body
from fastapi_restful.cbv import cbv

from app.auth.services import AuthService
from app.containers import AppContainers
from app.common.server import APIResponse
from app.google.services import GoogleService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@cbv(router)
class AuthEndpoint:

    @router.get(
        "/authorization-url",
        description="구글 로그인 URL을 반환합니다.",
    )
    @inject
    async def get_authorization_url(
        self,
        google_service: GoogleService = Depends(Provide[AppContainers.google.service]),
    ) -> APIResponse[dict]:
        authorization_url = await google_service.get_authorization_url()
        return APIResponse(
            message="구글 로그인 URL을 성공적으로 반환했습니다.",
            data={
                "authorization_url": authorization_url,
            },
        )

    @router.post(
        "/login",
        description="구글 로그인 후 사용자 정보를 반환합니다. (안되어있으면 자동가입)",
    )
    @inject
    async def login(
        self,
        code: str = Body(..., embed=True),
        auth_service: AuthService = Depends(Provide[AppContainers.auth.service]),
    ) -> APIResponse[dict]:
        access_token, new_register = await auth_service.login(code)
        return APIResponse(
            message="구글 로그인에 성공했습니다.",
            data={
                "access_token": access_token,
                "new_register": new_register,
            },
        )
