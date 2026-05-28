# galeria/domain/protocols/super_like.py
"""Protocolo estrutural para dados de superintendente."""

from collections.abc import Sequence
from pathlib import Path
from typing import Any, Protocol


class SuperLike(Protocol):
    """Contrato mínimo consumido por componentes de detalhe e galeria."""

    @property
    def id(self) -> str: ...

    @property
    def nome(self) -> str: ...

    @property
    def foto(self) -> Path | str | None: ...

    @property
    def timeline(self) -> Path | str | None: ...

    @property
    def periodo(self) -> str | None: ...

    @property
    def historias(self) -> Sequence[str] | None: ...

    @property
    def timeline_points(self) -> Sequence[Any] | None: ...
