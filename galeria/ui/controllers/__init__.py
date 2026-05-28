# galeria/ui/controllers/__init__.py
"""Controladores de estado usados pelas views e componentes de UI."""

from .auto_time_controller import AutoTimeoutController
from .gallery_scroll_controller import GalleryScrollController
from .slide_controller import SlideController
from .super_detail_controller import SuperDetailController

__all__ = [
    "AutoTimeoutController",
    "GalleryScrollController",
    "SlideController",
    "SuperDetailController",
]
