# galeria/ui/utils/flet_save.py
"""Chamadas auxiliares para atualizar controles Flet com segurança."""

import logging

import flet as ft

logger = logging.getLogger(__name__)


def safe_update(control: ft.Control) -> bool:
    """Atualiza um controle e ignora apenas o caso de ainda não estar montado."""
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
