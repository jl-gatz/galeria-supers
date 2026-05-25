# galeria/domain/services.py


from .models import Era, Super
from .super_repository import InterfaceSuperRepository


class SuperService:
    def __init__(self, repository: InterfaceSuperRepository):
        self.repository = repository

    # -------------------------
    # leitura
    # -------------------------

    def listar_supers(self) -> list[Super]:
        """
        Retorna todos os supers, incluindo placeholders (_blank),
        pois a UI depende deles para layout.
        """
        return self.repository.listar()

    def listar_supers_visiveis(self) -> list[Super]:
        """
        Retorna apenas supers válidos (sem _blank).
        Útil para listagens lógicas (não visuais).
        """
        return [s for s in self.listar_supers() if not self.is_blank(s)]

    def obter_super(self, super_id: str) -> Super | None:
        return self.repository.obter_por_id(super_id)

    def listar_eras(self) -> list[Era]:
        return self.repository.listar_eras()

    def obter_era(self, era_id: str) -> Era | None:
        return self.repository.obter_era(era_id)

    def obter_theme_da_era(self, era_id: str) -> str | None:
        return self.repository.obter_theme_da_era(era_id)

    # -------------------------
    # regras de domínio
    # -------------------------

    def is_blank(self, super_data: Super) -> bool:
        """
        Define se o item é um placeholder usado para layout.
        """
        return getattr(super_data, "nome", None) == "_blank"

    def pode_abrir(self, super_data: Super) -> bool:
        """
        Define se o card pode ser clicado/aberto.
        """
        return not self.is_blank(super_data)
