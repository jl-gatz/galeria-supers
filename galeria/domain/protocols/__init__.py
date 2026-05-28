# galeria/domain/protocols/__init__.py
"""Protocolos públicos usados para desacoplar camadas."""

from .gallery_service_like import GalleryServiceLike
from .super_like import SuperLike
from .super_service_like import SuperServiceLike

__all__ = [
    "GalleryServiceLike",
    "SuperLike",
    "SuperServiceLike",
]
