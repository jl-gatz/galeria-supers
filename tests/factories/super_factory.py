from tests.stubs.super_stub import SuperStub


class SuperFactory:
    @staticmethod
    def build(i: int) -> SuperStub:
        return SuperStub(
            id=f"super-{i}",
            nome=f"Super {i}",
            foto=f"/images/super{i}.png",
            timeline=f"/timeline/super{i}.png",
            timeline_points=None,
            historias=None,
        )

    @staticmethod
    def batch(n: int) -> list[SuperStub]:
        return [SuperFactory.build(i) for i in range(n)]
