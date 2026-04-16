# galeria/ui/utils/flet_save.py

import logging

import flet as ft

logger = logging.getLogger(__name__)


def safe_update(control: ft.Control) -> bool:
    """
    Tenta executar control.update() de forma segura.

    Retorna:
        True  -> update executado com sucesso
        False -> control ainda não está montado (ignorado)

    Levanta:
        RuntimeError -> se for um erro inesperado
    """
    try:
        control.update()
        return True

    except RuntimeError as e:
        msg = str(e)

        if "Control must be added to the page first" in msg:
            logger.debug("safe_update skipped: control not mounted yet")
            return False

        logger.exception("Unexpected error during control.update()")
        raise
