# galeria/domain/services.py
"""Serviços de domínio para leitura e regras de superintendentes."""

from .models import Era, Super
from .super_repository import InterfaceSuperRepository


class SuperService:
    """Orquestra acesso ao repositório e regras simples de domínio."""

    def __init__(self, repository: InterfaceSuperRepository):
        """Recebe o repositório usado pelas operações de domínio."""
        self.repository = repository

    # -------------------------
    # leitura
    # -------------------------

    def listar_supers(self) -> list[Super]:
        """Retorna todos os supers, incluindo placeholders usados pelo layout."""
        return self.repository.listar()

    def listar_supers_visiveis(self) -> list[Super]:
        """Retorna apenas supers válidos, sem placeholders de layout."""
        return [s for s in self.listar_supers() if not self.is_blank(s)]

    def obter_super(self, super_id: str) -> Super | None:
        """Obtém um superintendente pelo identificador."""
        return self.repository.obter_por_id(super_id)

    def listar_eras(self) -> list[Era]:
        """Lista as eras institucionais disponíveis."""
        return self.repository.listar_eras()

    def obter_era(self, era_id: str) -> Era | None:
        """Obtém uma era pelo identificador."""
        return self.repository.obter_era(era_id)

    def obter_theme_da_era(self, era_id: str) -> str | None:
        """Retorna o identificador de tema associado a uma era."""
        return self.repository.obter_theme_da_era(era_id)

    # -------------------------
    # regras de domínio
    # -------------------------

    def is_blank(self, super_data: Super) -> bool:
        """Indica se o super é um placeholder visual da galeria."""
        return getattr(super_data, "nome", None) == "_blank"

    def pode_abrir(self, super_data: Super) -> bool:
        """Indica se o card do super pode abrir a visão de detalhe."""
        return not self.is_blank(super_data)

    def build_image_path(self, super_data: Super) -> str | None:
        """Retorna o caminho de imagem já resolvido pelo repositório."""
        return super_data.foto

    def build_timeline_path(self, super_data: Super) -> str | None:
        """Retorna o caminho de timeline já resolvido pelo repositório."""
        return super_data.timeline
