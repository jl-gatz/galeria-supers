# tests/utils/snapshot.py


# tests/utils/snapshot.py
from tests.utils.renderers import register_default_renderers
from tests.utils.snapshot_config import SnapshotConfig
from tests.utils.snapshot_presets import STRUCTURE_V1
from tests.utils.tree_render_registry import registry
from tests.utils.tree_serializer import serialize_tree
from tests.utils.types import SnapshotLike

# garante que os renderers estão registrados
register_default_renderers()


def assert_tree_snapshot(
    view: object,
    snapshot: SnapshotLike,
    config: SnapshotConfig = STRUCTURE_V1,
    name: str = "gallery",
    modes: tuple[str, ...] = ("json", "simple"),
) -> None:
    tree = serialize_tree(view, config)

    for mode in modes:
        output = registry.render(mode, tree)
        filename = f"{name}_{mode}.txt" if mode == "simple" else f"{name}_{config.version}.json"

        snapshot.assert_match(output, filename)
