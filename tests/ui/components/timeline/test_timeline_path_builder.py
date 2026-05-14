# tests/ui/components/timeline/test_timeline_path_builder.py

import math

import pytest

from galeria.ui.components.timeline.utils import PathBuilder


def test_path_builder_returns_empty_list_for_empty_points():
    builder = PathBuilder()

    assert builder.build_path([]) == []


def test_path_builder_returns_single_valid_point_without_interpolation():
    builder = PathBuilder()
    point = [(10, 20)]

    assert builder.build_path(point) == point


def test_path_builder_sanitizes_invalid_points():
    builder = PathBuilder(mode="linear")

    points = [
        (10, 20),
        (None, 20),
        (10, None),
        (math.nan, 20),
        (10, math.nan),
        (math.inf, 20),
        (10, math.inf),
        (30, 40),
    ]

    assert builder.build_path(points) == [(10, 20), (30, 40)]


def test_path_builder_linear_mode_returns_sanitized_points():
    builder = PathBuilder(mode="linear")
    points = [(10, 20), (30, 40), (50, 10)]

    assert builder.build_path(points) == points


def test_path_builder_unknown_mode_falls_back_to_points():
    builder = PathBuilder(mode="unknown")
    points = [(10, 20), (30, 40), (50, 10)]

    assert builder.build_path(points) == points


def test_path_builder_smooth_mode_generates_curve_with_same_endpoints():
    builder = PathBuilder(mode="smooth")
    points = [(10, 20), (30, 40), (50, 10)]

    curve = builder.build_path(points)

    assert len(curve) > len(points)
    assert curve[0] == pytest.approx(points[0])
    assert curve[-1] == pytest.approx(points[-1])


def test_path_builder_infinity_mode_generates_curve_with_same_endpoints():
    builder = PathBuilder(mode="infinity")
    points = [(10, 20), (30, 40), (50, 10)]

    curve = builder.build_path(points)

    assert len(curve) > len(points)
    assert curve[0] == pytest.approx(points[0])
    assert curve[-1] == pytest.approx(points[-1])
