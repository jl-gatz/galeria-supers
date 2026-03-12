# tests/harness/tree_inspector.py

import flet as ft


def inspect_tree(control: ft.Control, indent=0):

    prefix = " " * indent
    name = control.__class__.__name__
    cid = getattr(control, "id", None)

    if cid:
        print(f"{prefix}{name} id={cid}")
    else:
        print(f"{prefix}{name}")

    if hasattr(control, "controls") and control.controls:
        for child in control.controls:
            inspect_tree(child, indent + 2)

    if hasattr(control, "content") and control.content:
        inspect_tree(control.content, indent + 2)
