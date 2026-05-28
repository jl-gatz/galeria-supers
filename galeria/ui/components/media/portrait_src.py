# galeria/ui/components/media/portrait_src.py
"""Normalização de caminhos de retratos usados pela UI."""

from pathlib import Path, PurePosixPath


def themed_portrait_src(src: str | Path | None) -> str | None:
    """Converte um caminho de retrato para formato POSIX aceito pelo Flet."""
    if src is None:
        return None

    path = PurePosixPath(str(src).replace("\\", "/"))
    return path.as_posix()
