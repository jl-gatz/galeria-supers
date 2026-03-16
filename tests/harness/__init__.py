# tests/harness/__init__.py

"""
Harness de testes para aplicações Flet.

Este pacote fornece utilitários para:

* montar controles em ambiente de teste
* navegar na árvore de controles
* executar queries CSS-like
* interagir com controles
* depurar visualmente a árvore usando Rich
"""

# Core do harness

# Query helpers
# from .control_query import ControlQuery

# Debug visual
from debug.render_summary import render_summary
from debug.rich_debug import render_node, render_query, render_tree

from .flet_harness import FletTestHarness

# Interações de teste
from .interactions import (
    change_text,
    click,
)

# Engine de seleção
from .selector_engine import SelectorEngine

# Navegação da árvore
from .tree_inspector import TreeInspector

__all__ = [
    "FletTestHarness",
    "SelectorEngine",
    "TreeInspector",
    "change_text",
    "click",
    "render_node",
    "render_query",
    "render_summary",
    "render_tree",
]
