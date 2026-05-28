# galeria/ui/theme/models.py
"""Modelos imutáveis que definem os tokens de tema da interface."""

from dataclasses import dataclass

import flet as ft

from galeria.ui.theme.styles import ComponentStyles

# =========================================================
# 🎨 SUBGRUPOS DE CORES
# =========================================================


@dataclass(frozen=True)
class BaseColors:
    """Cores de fundo e superfícies principais."""

    background: str
    surface: str
    surface_variant: str


@dataclass(frozen=True)
class TextColors:
    """Cores usadas em textos primários, secundários e invertidos."""

    primary: str
    secondary: str
    inverse: str


@dataclass(frozen=True)
class AccentColors:
    """Cores de destaque e contraste do tema."""

    primary: str
    secondary: str
    contrast: str


@dataclass(frozen=True)
class UIColors:
    """Cores auxiliares para bordas e sombras."""

    border: str
    shadow: str


@dataclass(frozen=True)
class ButtonColors:
    """Cores de botões e estados relacionados."""

    bg: str
    fg: str
    hover: str


@dataclass(frozen=True)
class TimelineColors:
    """Cores base usadas pela timeline."""

    line: str
    point: str
    point_active: str


@dataclass(frozen=True)
class ImageTheme:
    """Configurações visuais para imagens e máscaras."""

    portrait_tint: str | None = None
    portrait_blend_mode: ft.BlendMode | None = None
    portrait_opacity: float = 1.0
    caption_mask_tint: str = "#000000"
    caption_mask_blend_mode: ft.BlendMode = ft.BlendMode.SRC_IN
    caption_mask_opacity: float = 1.0


@dataclass(frozen=True)
class LogoTheme:
    """Configurações visuais para logos institucionais."""

    variant: str = "official"
    tint: str | None = None
    blend_mode: ft.BlendMode | None = None
    opacity: float = 1.0


# =========================================================
# ✍️ TIPOGRAFIA
# =========================================================


@dataclass(frozen=True)
class Typography:
    """Escala tipográfica e pesos usados pelo tema."""

    font_family: str

    display: int
    h1: int
    h2: int
    body: int
    small: int

    weight_regular: str | ft.FontWeight
    weight_medium: str | ft.FontWeight
    weight_bold: str | ft.FontWeight


# =========================================================
# 🖼️ GALLERY
# =========================================================


@dataclass(frozen=True)
class GalleryTheme:
    """Tokens de layout e interação da tela de galeria."""

    card_width: int
    card_height: int
    visible_cards: int

    h_spacing: int
    v_spacing: int
    padding: int
    max_width: int

    image_overlay: str
    hover_overlay: str
    title: str = "Galeria de Superintendentes"


# =========================================================
# 🧾 HEADER
# =========================================================


@dataclass(frozen=True)
class HeaderTheme:
    """Tokens do cabeçalho da visão de detalhe."""

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
    """Tokens específicos da superfície de detalhe."""

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
    """Escala de espaçamentos reutilizável."""

    xs: int = 8
    sm: int = 16
    md: int = 24
    lg: int = 40
    xl: int = 64


@dataclass(frozen=True)
class Radius:
    """Escala de raios de borda reutilizável."""

    sm: int = 8
    md: int = 16
    lg: int = 24


# =========================================================
# 🧠 THEME PRINCIPAL
# =========================================================


@dataclass(frozen=True)
class Theme:
    """Tema completo consumido por views, componentes e controladores."""

    id: str
    title: str

    # 🎨 cores base (mantidas)
    base: BaseColors
    overlay: str

    text: TextColors
    accent: AccentColors

    ui: UIColors
    button: ButtonColors

    timeline: TimelineColors
    image: ImageTheme
    logo: LogoTheme

    # ✍️ tipografia (NOVO)
    typography: Typography

    # 🧱 layout tokens (NOVO)
    spacing: Spacing
    radius: Radius
    styles: ComponentStyles

    # 🖼️ subtemas (NOVO)
    gallery: GalleryTheme
    header: HeaderTheme
    super_detail: SuperDetailTheme
