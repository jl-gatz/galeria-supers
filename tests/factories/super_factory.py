# tests/factories/super_factory.py

from galeria.domain.models import Super
from tests.stubs.super_stub import SuperStub


class SuperFactory:
    @staticmethod
    def build(i: int) -> Super:

        return SuperStub(
            id=f"super-{i}",
            nome=f"Super {i}",
            foto=f"/images/super{i}.png",
            timeline=f"/timeline/super{i}.png",
            timeline_points=None,
            historias=None,
        )

    @staticmethod
    def batch(n: int):

        return [SuperFactory.build(i) for i in range(n)]
