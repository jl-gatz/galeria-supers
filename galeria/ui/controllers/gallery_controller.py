from galeria.infrastructure.repositories.super_repository import SuperRepository


class GalleryController:
    def __init__(self):
        self.repo = SuperRepository()
        self.supers = self.repo.listar()

    def get_supers(self):
        return self.supers
