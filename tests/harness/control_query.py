# tests/harness/control_query.py

from collections.abc import Iterator

from tests.utils.types import HasContent, HasControls, HasValue


def walk(control: object) -> Iterator[object]:

    yield control

    if isinstance(control, HasControls) and control.controls:
        for child in control.controls:
            yield from walk(child)

    if isinstance(control, HasContent) and control.content:
        yield from walk(control.content)


def find_by_type(root: object, control_type: type[object]) -> list[object]:

    return [c for c in walk(root) if isinstance(c, control_type)]


def find_by_id(root: object, cid: object) -> object | None:

    for c in walk(root):
        if getattr(c, "id", None) == cid:
            return c

    return None


def find_by_text(root: object, text: object) -> list[object]:

    results: list[object] = []

    for c in walk(root):
        if isinstance(c, HasValue) and c.value == text:
            results.append(c)

    return results
