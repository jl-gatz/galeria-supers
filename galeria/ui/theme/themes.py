# galeria/ui/theme/themes.py


from galeria.ui.theme import RED_55
from galeria.ui.theme.colors import BLACK, BLUE_55, BLUE_DARK, PRIMARY_BLUE, PRIMARY_RED

from .models import Theme

CCUEC_THEME = Theme(
    title="Galeria de Superintendentes do CCUEC",
    background=BLUE_55,
    primary=PRIMARY_BLUE,
    text=BLUE_DARK,
)

DETIC_THEME = Theme(
    title="Galeria de Superintendentes da Detic",
    background=RED_55,
    primary=PRIMARY_RED,
    text=BLACK,
)
