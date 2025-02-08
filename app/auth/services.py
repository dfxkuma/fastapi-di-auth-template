from jwt import encode as jwt_encode, decode as jwt_decode, PyJWTError
from passlib.context import CryptContext
import aiogoogle

from app.common.utils.env_validator import get_settings
from app.common.utils.logger import use_logger
from app.google.services import GoogleService
from app.common.exceptions import AuthenticateFailed

from app.members.entities import MemberEntity
from app.common.types import USER_ID
from app.members.repository import MemberRepository

logger = use_logger("auth_service")
settings = get_settings()


async def get_phone_by_token(token: str) -> str:
    payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    return payload.get("phone")


class AuthService:
    def __init__(
        self, member_repository: MemberRepository, google_service: GoogleService
    ) -> None:
        self.member_repository = member_repository
        self.google_service = google_service
        self.hashed_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_from_credential(self, email: str) -> MemberEntity | None:
        entity = await self.member_repository.get_by_email(email)
        return entity

    @staticmethod
    async def create_access_token(entity_id: str) -> str:
        encoded_jwt = jwt_encode(
            {"uid": entity_id},
            settings.JWT_SECRET_KEY,
            algorithm="HS256",
        )
        return encoded_jwt

    @staticmethod
    async def get_user_id_from_token(token: str) -> USER_ID:
        payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload.get("uid")

    @staticmethod
    def get_access_token_payload(token: str) -> tuple[str, str] or None:
        try:
            payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            return payload.get("uid"), payload.get("hn")
        except PyJWTError:
            return None

    async def login(self, code: str) -> tuple[str, bool]:  # access_token, new_register
        try:
            token_data = await self.google_service.fetch_user_credentials(code)
            user_data = await self.google_service.fetch_user_info(self.google_service.build_user_credentials(token_data["access_token"]))
        except aiogoogle.excs.HTTPError as _:
            raise AuthenticateFailed(
                message="구글 로그인에 실패했습니다. 다시 시도해주세요."
            )

        email = user_data.get("email")
        new_register = False
        if not await self.member_repository.exist(email):
            await self.member_repository.create(nickname=user_data["name"], email=email)
            new_register = True
        member_entity = await self.member_repository.get_by_email(email)
        access_token = await self.create_access_token(str(member_entity.id))
        return access_token, new_register
