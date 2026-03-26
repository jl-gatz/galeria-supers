from tests.stubs.fake_super import FakeSuper


def test_starts_with_first_slide(make_controller: FakeSuper):
    controller: FakeSuper = make_controller(["A", "B", "C"])

    assert controller.current == "A"


def test_next_moves_forward(make_controller: FakeSuper):
    controller: FakeSuper = make_controller(["A", "B", "C"])

    moved = controller.next()

    assert moved is True
    assert controller.current == "B"


def test_next_at_end_returns_false(make_controller: FakeSuper):
    controller: FakeSuper = make_controller(["A", "B"])

    controller.next()  # vai para B
    moved = controller.next()  # tenta ir além

    assert moved is False
    assert controller.current == "B"


def test_prev_moves_backward(make_controller: FakeSuper):
    controller: FakeSuper = make_controller(["A", "B", "C"])

    controller.next()  # B
    moved = controller.prev()

    assert moved is True
    assert controller.current == "A"


def test_prev_at_start_returns_false(make_controller: FakeSuper):
    controller: FakeSuper = make_controller(["A", "B"])

    moved = controller.prev()

    assert moved is False
    assert controller.current == "A"


def test_goto_valid_index(make_controller: FakeSuper):
    controller: FakeSuper = make_controller(["A", "B", "C"])

    moved = controller.goto(2)

    assert moved is True
    assert controller.current == "C"


def test_sequence_navigation(make_controller: FakeSuper):
    controller: FakeSuper = make_controller(["A", "B", "C"])

    controller.next()  # B
    controller.next()  # C
    controller.prev()  # B

    assert controller.current == "B"
