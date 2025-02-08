from dependency_injector import containers, providers

from app.auth.services import AuthService


class AuthContainer(containers.DeclarativeContainer):
    google_service = providers.Dependency()
    member_repository = providers.Dependency()

    service = providers.Factory(
        AuthService, google_service=google_service, member_repository=member_repository
    )
