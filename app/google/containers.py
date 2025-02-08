from dependency_injector import containers, providers

from app.google.services import GoogleService


class GoogleContainer(containers.DeclarativeContainer):
    service: GoogleService = providers.Singleton(GoogleService)
