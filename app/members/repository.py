from app.members.entities import MemberEntity


class MemberRepository:

    @classmethod
    async def create(cls, nickname: str, email: str) -> MemberEntity:
        return await MemberEntity.create(nickname=nickname, email=email)

    @classmethod
    async def get_by_email(cls, email: str) -> MemberEntity:
        return await MemberEntity.get_or_none(email=email)

    @classmethod
    async def get_by_id(cls, id: str) -> MemberEntity:
        return await MemberEntity.get(id=id)

    @classmethod
    async def exist(cls, email: str) -> bool:
        return await MemberEntity.exists(email=email)
