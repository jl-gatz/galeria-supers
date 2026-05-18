# galeria/ui/theme/themes.py

import flet as ft

from galeria.ui.theme.models import (
    AccentColors,
    BaseColors,
    ButtonColors,
    GalleryTheme,
    HeaderTheme,
    ImageTheme,
    LogoTheme,
    Radius,
    Spacing,
    SuperDetailTheme,
    TextColors,
    Theme,
    TimelineColors,
    Typography,
    UIColors,
)
from galeria.ui.theme.styles import default_component_styles


# =========================================================
# MÉTODOS PARA TIPOGRAFIA E OUTROS ESTILOS DINÂMICOS
# ==========================================================
def create_typography(
    font_family: str = "Montserrat",
    display: int = 96,
    h1: int = 72,
    h2: int = 36,
    body: int = 30,
    small: int = 16,
    weight_regular: ft.FontWeight = ft.FontWeight.W_400,
    weight_medium: ft.FontWeight = ft.FontWeight.W_500,
    weight_bold: ft.FontWeight = ft.FontWeight.W_700,
) -> Typography:
    return Typography(
        font_family=font_family,
        display=display,
        h1=h1,
        h2=h2,
        body=body,
        small=small,
        weight_regular=weight_regular,
        weight_medium=weight_medium,
        weight_bold=weight_bold,
    )


# ==========================================================
# 🧱 BASE COMPARTILHADA (evita repetição)
# ==========================================================

BASE_COLORS = BaseColors(
    background="#FFFFFF",
    surface="#FFFFFF",
    surface_variant="#F5F5F5",
)

UI_BASE = UIColors(
    border="#3A3D3E",
    shadow="rgba(0,0,0,0.5)",
)

TIMELINE_BASE = "#3A3D3E"
TIMELINE_POINT = "#9B9292"

SPACING = Spacing()
RADIUS = Radius()
STYLES = default_component_styles()


def official_logo_theme() -> LogoTheme:
    return LogoTheme(
        variant="official",
        tint=None,
        blend_mode=None,
        opacity=1.0,
    )


# ==========================================================
# 🔴 DETIC
# ==========================================================

DETIC_RED = "#E10514"
DETIC_BLACK = "#161819"

DETIC_THEME = Theme(
    id="detic_era",
    title="DETIC",
    base=BaseColors(
        background="#FFFFFF",
        surface="#FFFFFF",
        surface_variant="#F5F5F5",
    ),
    overlay="rgba(0,0,0,0.4)",
    text=TextColors(
        primary=DETIC_BLACK,
        secondary="#4B5563",
        inverse="#FFFFFF",
    ),
    accent=AccentColors(
        primary=DETIC_RED,
        secondary="#FECED1",
        contrast="#FFFFFF",
    ),
    ui=UI_BASE,
    button=ButtonColors(
        bg=DETIC_RED,
        fg="#FFFFFF",
        hover="#C00410",
    ),
    timeline=TimelineColors(
        line=DETIC_RED,
        point="#FECED1",
        point_active="#7D030B",
    ),
    image=ImageTheme(
        caption_mask_tint="#FA0511",
        caption_mask_blend_mode=ft.BlendMode.SRC_IN,
        caption_mask_opacity=0.65,
    ),
    logo=official_logo_theme(),
    typography=create_typography(
        font_family="Montserrat",
        display=96,
        h1=72,
        h2=42,
        body=30,
        small=16,
        weight_regular="Montserrat-Medium",
        weight_medium="Montserrat-Bold",
        weight_bold="Montserrat-BLACK",
    ),
    spacing=SPACING,
    radius=RADIUS,
    styles=STYLES,
    gallery=GalleryTheme(
        card_width=300,
        card_height=394,
        visible_cards=4,
        h_spacing=160,
        v_spacing=40,
        padding=20,
        max_width=1920,
        image_overlay="rgba(0,0,0,0.15)",
        hover_overlay="rgba(225,5,20,0.10)",
    ),
    header=HeaderTheme(
        height=120,
        title_size=32,
        subtitle_size=16,
        background="#FFFFFF",
        text_color=DETIC_RED,
        accent=DETIC_RED,
    ),
    super_detail=SuperDetailTheme(
        content_width=1000,
        image_height=420,
        background="#FFFFFF",
        overlay="rgba(225,5,20,0.08)",
        title_size=34,
        body_size=18,
        timeline_color=DETIC_RED,
        highlight=DETIC_RED,
    ),
)


# ==========================================================
# 🔵 CCUEC (ajustado para azul institucional)
# ==========================================================

CCUEC_BLUE = "#0513E1"  # <---- confirmar CORES aqui
CCUEC_DARK = "#030B7D"  # <---- confirmar CORES aqui
CCUEC_ACCENT = "#EAB308"
CCUEC_BG = "#FFFBF1"  # creme leve

CCUEC_THEME = Theme(
    id="ccuec_era",
    title="CCUEC",
    base=BaseColors(
        background=CCUEC_BG,
        surface="#FFFFFF",
        surface_variant="#F3F4F6",
    ),
    overlay="rgba(0,0,0,0.4)",
    text=TextColors(
        primary=CCUEC_DARK,
        secondary="#475569",
        inverse="#FFFFFF",
    ),
    accent=AccentColors(
        primary=CCUEC_BLUE,
        secondary="#CED1FE",
        contrast="#FFFFFF",
    ),
    ui=UI_BASE,
    button=ButtonColors(
        bg=CCUEC_BLUE,
        fg="#FFFFFF",
        hover="#1E40AF",
    ),
    timeline=TimelineColors(
        line=CCUEC_BLUE,
        point="#CED1FE",
        point_active=CCUEC_ACCENT,
    ),
    image=ImageTheme(
        caption_mask_tint="#0461E4",
        caption_mask_blend_mode=ft.BlendMode.SRC_IN,
        caption_mask_opacity=0.65,
    ),
    logo=official_logo_theme(),
    typography=create_typography(
        font_family="Lora-Regular",
        display=96,
        h1=72,
        h2=42,
        body=30,
        small=16,
        weight_regular="Lora-Medium",
        weight_medium="Lora-SemiBold",
        weight_bold="Lora-Bold",
    ),
    spacing=SPACING,
    radius=RADIUS,
    styles=STYLES,
    gallery=GalleryTheme(
        card_width=300,
        card_height=394,
        visible_cards=4,
        h_spacing=160,
        v_spacing=40,
        padding=20,
        max_width=1920,
        image_overlay="rgba(0,0,0,0.1)",
        hover_overlay="rgba(29,78,216,0.10)",
    ),
    header=HeaderTheme(
        height=120,
        title_size=32,
        subtitle_size=16,
        background=CCUEC_BG,
        text_color=CCUEC_BLUE,
        accent=CCUEC_ACCENT,
    ),
    super_detail=SuperDetailTheme(
        content_width=1000,
        image_height=420,
        background=CCUEC_BG,
        overlay="rgba(29,78,216,0.08)",
        title_size=34,
        body_size=18,
        timeline_color=CCUEC_BLUE,
        highlight=CCUEC_ACCENT,
    ),
)


# ==========================================================
# 🟢 GREENISH (novo tema — mais vibrante e moderno)
# ==========================================================

GREEN_PRIMARY = "#22C55E"
GREEN_ACCENT = "#4ADE80"
GREEN_BG = "#0B1F1A"
GREEN_SURFACE = "#0F2A24"
GREEN_TEXT = "#E6F4F1"

GREENISH_THEME = Theme(
    id="greenish",
    title="GREENISH",
    base=BaseColors(
        background=GREEN_BG,
        surface=GREEN_SURFACE,
        surface_variant="#13332C",
    ),
    overlay="rgba(0,0,0,0.6)",
    text=TextColors(
        primary=GREEN_TEXT,
        secondary="#9CA3AF",
        inverse="#D7F2F3",
    ),
    accent=AccentColors(
        primary=GREEN_PRIMARY,
        secondary="#4ADE80",
        contrast="#003B2F",
    ),
    ui=UI_BASE,
    button=ButtonColors(
        bg=GREEN_PRIMARY,
        fg="#003B2F",
        hover="#16A34A",
    ),
    timeline=TimelineColors(
        line=GREEN_PRIMARY,
        point="#065F46",
        point_active=GREEN_ACCENT,
    ),
    image=ImageTheme(
        caption_mask_tint="#14F18A",
        caption_mask_blend_mode=ft.BlendMode.SRC_IN,
        caption_mask_opacity=0.65,
    ),
    logo=official_logo_theme(),
    typography=create_typography(
        font_family="Manrope-Regular",
        display=96,
        h1=72,
        h2=42,
        body=30,
        small=16,
        weight_regular="Manrope-Regular",
        weight_medium="Manrope-Bold",
        weight_bold="Manrope-ExtraBold",
    ),
    spacing=SPACING,
    radius=RADIUS,
    styles=STYLES,
    gallery=GalleryTheme(
        card_width=300,
        card_height=394,
        visible_cards=4,
        h_spacing=160,
        v_spacing=40,
        padding=20,
        max_width=1920,
        image_overlay="rgba(0,0,0,0.35)",
        hover_overlay="rgba(34,197,94,0.15)",
    ),
    header=HeaderTheme(
        height=120,
        title_size=32,
        subtitle_size=16,
        background=GREEN_BG,
        text_color=GREEN_PRIMARY,
        accent=GREEN_ACCENT,
    ),
    super_detail=SuperDetailTheme(
        content_width=1000,
        image_height=420,
        background=GREEN_BG,
        overlay="rgba(34,197,94,0.08)",
        title_size=34,
        body_size=18,
        timeline_color=GREEN_PRIMARY,
        highlight=GREEN_ACCENT,
    ),
)


# ==========================================================
# 🟣 FUTURO: ROYAL (tema mais luxuoso, inspirado em roxo e dourado)
# ==========================================================
