from dependency_injector import containers, providers

from app.members.repository import MemberRepository


class MemberContainer(containers.DeclarativeContainer):
    repository: MemberRepository = providers.Singleton(MemberRepository)
