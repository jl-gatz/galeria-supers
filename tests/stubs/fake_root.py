from tests.stubs import FakePage


class FakeRoot:
    def __init__(self, page: FakePage):
        self.page = page
        self.overlay_shown = None
        self.overlay_hidden = None
        self.history = []

    def show_overlay(self, component):
        # monta o componente na "árvore"
        self.overlay_shown = component

        component.parent = self
        self.page.add(component)  # garante acesso a page

        # simula lifecycle do Flet
        if hasattr(component, "did_mount"):
            component.did_mount()

        self.history.append(("show", component))

    def hide_overlay(self, component):
        self.overlay_hidden = component

        # simula teardown (equivalente a unmount)
        if hasattr(component, "will_unmount"):
            component.will_unmount()

        # fallback comum (caso não tenha lifecycle explícito)
        if hasattr(component, "auto_controller"):
            component.auto_controller.stop()

        # remove da árvore
        if component in self.page.controls:
            self.page.controls.remove(component)

        component.parent = None

        self.history.append(("hide", component))
