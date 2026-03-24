class FakeRoot:
    def __init__(self):
        self.overlay_shown = None
        self.overlay_hidden = None

    def show_overlay(self, component):
        self.overlay_shown = component

    def hide_overlay(self, component):
        self.overlay_hidden = component
