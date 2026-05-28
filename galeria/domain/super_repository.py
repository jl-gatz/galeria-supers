# galeria/domain/super_repository.py
"""Contrato abstrato para repositórios de superintendentes."""

from abc import ABC, abstractmethod

from .models import Era, Super


class InterfaceSuperRepository(ABC):
    """Interface que a infraestrutura deve implementar para o domínio."""

    @abstractmethod
    def listar(self) -> list[Super]:
        """Lista todos os superintendentes disponíveis."""
        raise NotImplementedError

    @abstractmethod
    def obter_por_id(self, super_id: str) -> Super | None:
        """Obtém um superintendente pelo identificador."""
        raise NotImplementedError

    @abstractmethod
    def listar_eras(self) -> list[Era]:
        """Lista as eras institucionais disponíveis."""
        raise NotImplementedError

    @abstractmethod
    def obter_era(self, era_id: str) -> Era | None:
        """Obtém uma era pelo identificador."""
        raise NotImplementedError

    @abstractmethod
    def obter_theme_da_era(self, era_id: str) -> str | None:
        """Retorna o identificador de tema associado a uma era."""
        raise NotImplementedError
