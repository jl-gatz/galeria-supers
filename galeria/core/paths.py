# core/paths.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
PHOTOS_DIR = BASE_DIR / "assets" / "images" / "supers"
SUPERS_JSON = DATA_DIR / "supers.json"
LOGO_DETIC = "images/logos/logo-detic-4x.png"
LOGO_UNICAMP = "images/logos/Logo_Unicamp__0.png"
