# galeria/core/paths.py
"""Caminhos centrais para dados e assets da aplicação."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
PHOTOS_DIR = ASSETS_DIR / "images" / "supers" / "grayscale"
LOGOS_DIR = ASSETS_DIR / "images" / "logos"

SUPERS_JSON = DATA_DIR / "supers.json"
ERAS_JSON = DATA_DIR / "eras.json"

LOGO_DETIC = "images/logos/logo-detic-4x.png"
LOGO_UNICAMP = "images/logos/Logo_Unicamp__0.png"
SUPER_CAPTION_MASK = "images/masks/super-caption-mask.png"
IMAGES_URL = "images/supers/grayscale"
TIMELINE_URL = "images/timelines"
