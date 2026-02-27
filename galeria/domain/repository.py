from abc import ABC, abstractmethod
from collections.abc import Sequence

from .models import Super


class SuperRepository(ABC):
    @abstractmethod
    def listar(self) -> Sequence[Super]:
        raise NotImplementedError

    @abstractmethod
    def obter_por_id(self, super_id: str) -> Super | None:
        raise NotImplementedError
