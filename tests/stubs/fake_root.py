from typing import Protocol, cast, runtime_checkable

from tests.stubs import FakePage
from tests.stubs.flet_harness_to_page import Mountable, Unmountable


@runtime_checkable
class Stoppable(Protocol):
    def stop(self) -> None: ...


@runtime_checkable
class HasAutoController(Protocol):
    auto_controller: Stoppable


class HasParent(Protocol):
    parent: object | None


class FakeRoot:
    def __init__(self, page: FakePage) -> None:
        self.page = page
        self.overlay_shown: object | None = None
        self.overlay_hidden: object | None = None
        self.history: list[tuple[str, object]] = []

    def show_overlay(self, component: object) -> None:
        # monta o componente na "árvore"
        self.overlay_shown = component

        cast(HasParent, component).parent = self
        self.page.add(component)  # garante acesso a page

        # simula lifecycle do Flet
        if isinstance(component, Mountable):
            component.did_mount()

        self.history.append(("show", component))

    def hide_overlay(self, component: object) -> None:
        self.overlay_hidden = component

        # simula teardown (equivalente a unmount)
        if isinstance(component, Unmountable):
            component.will_unmount()

        # fallback comum (caso não tenha lifecycle explícito)
        if isinstance(component, HasAutoController):
            component.auto_controller.stop()

        # remove da árvore
        if component in self.page.controls:
            self.page.controls.remove(component)

        cast(HasParent, component).parent = None

        self.history.append(("hide", component))
