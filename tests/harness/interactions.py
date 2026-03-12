# tests/harness/interactions.py


def click(control):

    if hasattr(control, "on_click") and control.on_click:
        control.on_click(None)


def change_text(control, value):

    if hasattr(control, "value"):
        control.value = value

    if hasattr(control, "on_change") and control.on_change:
        control.on_change(None)
