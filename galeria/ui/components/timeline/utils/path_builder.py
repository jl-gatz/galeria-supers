# galeria/ui/components/timeline/utils/path_builder.py


import math

Segment = dict[str, tuple[float, float]]


def _safe(n: float) -> float:
    """Evita NaN / infinito (causa do erro do Flutter)."""
    if math.isnan(n) or math.isinf(n):
        return 0.0
    return n


def _clamp01(n: float) -> float:
    return max(0.0, min(1.0, n))


def build_partial_path(segments: list[Segment], progress: float) -> str:
    """
    Gera path SVG parcial baseado no progresso (0..1).
    Seguro contra valores inválidos.
    """

    if not segments:
        return ""

    progress = _clamp01(progress)

    total = len(segments)
    current = progress * total

    full_segments = int(current)
    remainder = current - full_segments

    path: list[str] = []

    # 🔹 Move inicial
    x0, y0 = segments[0]["start"]
    path.append(f"M {_safe(x0):.3f},{_safe(y0):.3f}")

    # 🔹 Segmentos completos
    for i in range(full_segments):
        s = segments[i]

        cp1x, cp1y = s["cp1"]
        cp2x, cp2y = s["cp2"]
        ex, ey = s["end"]

        path.append(
            f"C {_safe(cp1x):.3f},{_safe(cp1y):.3f} "
            f"{_safe(cp2x):.3f},{_safe(cp2y):.3f} "
            f"{_safe(ex):.3f},{_safe(ey):.3f}"
        )

    # 🔹 Segmento parcial
    if full_segments < total:
        s = segments[full_segments]

        sx, sy = s["start"]
        ex, ey = s["end"]

        # interpolação linear segura
        px = sx + (ex - sx) * remainder
        py = sy + (ey - sy) * remainder

        path.append(f"L {_safe(px):.3f},{_safe(py):.3f}")

    result = " ".join(path)

    # 🔥 DEBUG opcional
    if "nan" in result.lower():
        print("🚨 PATH INVÁLIDO:", result)

    return result
