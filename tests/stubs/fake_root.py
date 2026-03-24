class FakeRoot:
    def __init__(self):
        self.overlay_shown = None
        self.overlay_hidden = None
        self.history = []

    def show_overlay(self, component):
        self.overlay_shown = component
        self.history.append(("show", component))

    def hide_overlay(self, component):
        self.overlay_hidden = component
        self.history.append(("hide", component))
