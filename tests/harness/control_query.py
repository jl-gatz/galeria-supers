# tests/harness/control_query.py


def walk(control):

    yield control

    if hasattr(control, "controls") and control.controls:
        for child in control.controls:
            yield from walk(child)

    if hasattr(control, "content") and control.content:
        yield from walk(control.content)


def find_by_type(root, control_type):

    return [c for c in walk(root) if isinstance(c, control_type)]


def find_by_id(root, cid):

    for c in walk(root):
        if getattr(c, "id", None) == cid:
            return c

    return None


def find_by_text(root, text):

    results = []

    for c in walk(root):
        if hasattr(c, "value") and c.value == text:
            results.append(c)

    return results
