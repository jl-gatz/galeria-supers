from galeria.domain.models import Super
from galeria.domain.super_repository import InterfaceSuperRepository


class SuperService:
    def __init__(self, repository: InterfaceSuperRepository):
        self.repository = repository

    # -------------------------
    # leitura
    # -------------------------

    def listar_supers(self) -> list[Super]:
        return self.repository.listar()

    def obter_super(self, super_id: str) -> Super | None:
        return self.repository.obter_por_id(super_id)

    # -------------------------
    # regras de domínio
    # -------------------------

    def is_blank(self, super_data: Super) -> bool:
        return super_data.name == "_blank"

    def pode_abrir(self, super_data: Super) -> bool:
        return not self.is_blank(super_data)

    def build_image_path(self, super_data: Super) -> str:
        return f"images/supers/{super_data.foto}"

    def build_timeline_path(self, super_data: Super) -> str | None:
        return None if not super_data.timeline else super_data.timeline
