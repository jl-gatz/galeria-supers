class FakeSuper:
    def __call__(self):
        return self

    def __init__(self, historias: list[str]):
        self.historias = historias
