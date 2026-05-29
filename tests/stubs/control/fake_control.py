class FakeControl:
    def __init__(self) -> None:
        self.controls: list[object] = []
        self.visible = True
        self.content: object | None = None

    def update(self) -> None:
        pass
