from abc import ABC, abstractmethod

from .models import Era, Super


class InterfaceSuperRepository(ABC):
    @abstractmethod
    def listar(self) -> list[Super]:
        raise NotImplementedError

    @abstractmethod
    def obter_por_id(self, super_id: str) -> Super | None:
        raise NotImplementedError

    @abstractmethod
    def listar_eras(self) -> list[Era]:
        raise NotImplementedError

    @abstractmethod
    def obter_era(self, era_id: str) -> Era | None:
        raise NotImplementedError

    @abstractmethod
    def obter_theme_da_era(self, era_id: str) -> str | None:
        raise NotImplementedError
