from abc import ABC, abstractmethod

from .models import Super


class InterfaceSuperRepository(ABC):
    @abstractmethod
    def listar(self) -> list[Super]:
        raise NotImplementedError

    @abstractmethod
    def obter_por_id(self, super_id: str) -> Super | None:
        raise NotImplementedError
