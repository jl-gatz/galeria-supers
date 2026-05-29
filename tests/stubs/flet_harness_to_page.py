from contextlib import suppress
from typing import Protocol, TypeVar, runtime_checkable
from unittest.mock import PropertyMock

# -------------------------
# 🔌 Protocols (contratos)
# -------------------------


@runtime_checkable
class PageLike(Protocol):
    def add(self, *controls: object) -> None: ...
    def update(self) -> None: ...


@runtime_checkable
class Mountable(Protocol):
    def did_mount(self) -> None: ...


@runtime_checkable
class Unmountable(Protocol):
    def will_unmount(self) -> None: ...


# Tipo genérico de controle
T = TypeVar("T", bound=object)


# -------------------------
# 🚀 Helpers
# -------------------------


def attach_fake_page(control: object, fake_page: PageLike) -> None:
    """
    Injeta um fake_page em um controle Flet, sobrescrevendo
    a propriedade `page` (que é read-only no framework).
    """
    setattr(type(control), "page", PropertyMock(return_value=fake_page))  # noqa: B010


def mount[T](control: T, fake_page: PageLike) -> T:
    # 🔥 APLICAR ANTES DE QUALQUER COISA
    attach_fake_page(control, fake_page)

    # só depois adicionar à estrutura
    if hasattr(fake_page, "add"):
        fake_page.add(control)

    # lifecycle
    if isinstance(control, Mountable):
        control.did_mount()

    return control


def unmount(control: object) -> None:
    """
    Simula desmontagem completa de um controle:
    """
    if isinstance(control, Unmountable):
        control.will_unmount()

    # remove override da property (evita vazamento entre testes)
    if hasattr(type(control), "page"):
        with suppress(Exception):
            delattr(type(control), "page")
