# domain/protocols/gallery_service_like.py

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from galeria.domain import Super


class GalleryServiceLike(Protocol):
    def listar_supers(self) -> Sequence[Super]: ...
    def pode_abrir(self, super_data: Super) -> bool: ...
    def build_image_path(self, super_data: Super) -> Path | None: ...
    def build_timeline_path(self, super_data: Super) -> Path | None: ...
