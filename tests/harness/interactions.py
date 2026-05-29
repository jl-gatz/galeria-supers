# tests/harness/interactions.py

from tests.utils.types import Changeable, Clickable, HasValue


def click(control: object) -> None:

    if isinstance(control, Clickable) and control.on_click:
        control.on_click(None)


def change_text(control: object, value: object) -> None:

    if isinstance(control, HasValue):
        control.value = value

    if isinstance(control, Changeable) and control.on_change:
        control.on_change(None)
