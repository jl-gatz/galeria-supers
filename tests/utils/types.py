from collections.abc import Callable, Iterator, Sequence
from typing import Protocol, TypedDict, runtime_checkable

type Selector = str | type[object]
type EventHandler = Callable[[object | None], object]
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
type TreeProps = dict[str, JsonValue]


class SerializedNode(TypedDict):
    type: str
    props: TreeProps
    children: list["SerializedNode"]


type SerializedTree = SerializedNode | str


@runtime_checkable
class HasContent(Protocol):
    content: object | None


@runtime_checkable
class HasPrivateContent(Protocol):
    _content: object | None


@runtime_checkable
class HasControls(Protocol):
    controls: Sequence[object]


@runtime_checkable
class HasItems(Protocol):
    items: Sequence[object]


@runtime_checkable
class HasValue(Protocol):
    value: object


@runtime_checkable
class HasSrc(Protocol):
    src: object


@runtime_checkable
class HasKey(Protocol):
    key: object


@runtime_checkable
class HasText(Protocol):
    text: object


@runtime_checkable
class HasData(Protocol):
    data: object


@runtime_checkable
class HasSuperData(Protocol):
    super_data: object


@runtime_checkable
class Clickable(Protocol):
    on_click: EventHandler | None


@runtime_checkable
class Changeable(Protocol):
    on_change: EventHandler | None
    value: object


class InspectorLike(Protocol):
    def children(self, control: object) -> list[object]: ...
    def descendants(self, node: object) -> Iterator[object]: ...
    def format_tree(self, show_props: bool = True, max_depth: int | None = None) -> str: ...
    def rich_tree(self, show_props: bool = True, max_depth: int | None = None) -> object: ...


class SelectHarnessLike(Protocol):
    def select(self, selector: str) -> list[object]: ...


class SnapshotLike(Protocol):
    def assert_match(self, value: str, filename: str) -> None: ...


class TestPageLike(Protocol):
    controls: list[object]

    def add(self, *controls: object) -> None: ...
    def update(self, *controls: object) -> None: ...


@runtime_checkable
class AsyncUpdatable(Protocol):
    async def update_async(self) -> None: ...
