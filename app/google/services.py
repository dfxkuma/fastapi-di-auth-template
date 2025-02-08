import os

from aiohttp import ClientSession
from app.common.utils.env_validator import get_settings
from app.common.utils.logger import use_logger

from aiogoogle import Aiogoogle, auth as aiogoogle_auth
from aiogoogle.auth.creds import UserCreds

settings = get_settings()
logger = use_logger("google_service")


class GoogleScope:
    BASE_URL = "https://www.googleapis.com/auth"

    def __class_getitem__(cls, key: str) -> str:
        return f"{cls.BASE_URL}/{key}"


class GoogleService:
    def __init__(self) -> None:

        self.__google_credentials = aiogoogle_auth.creds.ClientCreds(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=[
                GoogleScope["userinfo.email"],
                GoogleScope["userinfo.profile"],
            ],
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
        )
        self._google_client = Aiogoogle(
            client_creds=self.__google_credentials,
        )
        self._request = ClientSession()

    async def get_authorization_url(self) -> str:
        return self._google_client.oauth2.authorization_url(
            access_type="online",
            include_granted_scopes=True,
            prompt="consent",
        )

    @staticmethod
    def build_user_credentials(access_token: str) -> UserCreds:
        return UserCreds(
            access_token=access_token,
        )

    async def fetch_user_credentials(self, code: str) -> dict:
        return await self._google_client.oauth2.build_user_creds(
            grant=code, client_creds=self.__google_credentials
        )

    async def fetch_user_info(self, user_credentials: dict) -> dict:
        return await self._google_client.oauth2.get_me_info(
            user_creds=user_credentials,
        )
