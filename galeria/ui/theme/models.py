# galeria/ui/theme/models.py

from dataclasses import dataclass

# =========================================================
# 🎨 SUBGRUPOS DE CORES
# =========================================================


@dataclass(frozen=True)
class BaseColors:
    background: str
    surface: str
    surface_variant: str


@dataclass(frozen=True)
class TextColors:
    primary: str
    secondary: str
    inverse: str


@dataclass(frozen=True)
class AccentColors:
    primary: str
    secondary: str
    contrast: str


@dataclass(frozen=True)
class UIColors:
    border: str
    shadow: str


@dataclass(frozen=True)
class ButtonColors:
    bg: str
    fg: str
    hover: str


@dataclass(frozen=True)
class TimelineColors:
    line: str
    point: str
    point_active: str


# =========================================================
# ✍️ TIPOGRAFIA
# =========================================================


@dataclass(frozen=True)
class Typography:
    font_family: str

    display: int
    h1: int
    h2: int
    body: int
    small: int

    weight_regular: int
    weight_medium: int
    weight_bold: int


# =========================================================
# 🖼️ GALLERY
# =========================================================


@dataclass(frozen=True)
class GalleryTheme:
    card_width: int
    card_height: int
    visible_cards: int

    h_spacing: int
    v_spacing: int
    padding: int
    max_width: int

    image_overlay: str
    hover_overlay: str


# =========================================================
# 🧾 HEADER
# =========================================================


@dataclass(frozen=True)
class HeaderTheme:
    height: int

    title_size: int
    subtitle_size: int

    background: str
    text_color: str
    accent: str


# =========================================================
# 🔍 SUPER DETAIL
# =========================================================


@dataclass(frozen=True)
class SuperDetailTheme:
    content_width: int
    image_height: int

    background: str
    overlay: str

    title_size: int
    body_size: int

    timeline_color: str
    highlight: str


# =========================================================
# 🧩 TOKENS DE LAYOUT (opcional mas recomendado)
# =========================================================


@dataclass(frozen=True)
class Spacing:
    xs: int = 8
    sm: int = 16
    md: int = 24
    lg: int = 40
    xl: int = 64


@dataclass(frozen=True)
class Radius:
    sm: int = 8
    md: int = 16
    lg: int = 24


# =========================================================
# 🧠 THEME PRINCIPAL
# =========================================================


@dataclass(frozen=True)
class Theme:
    title: str

    # 🎨 cores base (mantidas)
    base: BaseColors
    overlay: str

    text: TextColors
    accent: AccentColors

    ui: UIColors
    button: ButtonColors

    timeline: TimelineColors

    # ✍️ tipografia (NOVO)
    typography: Typography

    # 🧱 layout tokens (NOVO)
    spacing: Spacing
    radius: Radius

    # 🖼️ subtemas (NOVO)
    gallery: GalleryTheme
    header: HeaderTheme
    super_detail: SuperDetailTheme
