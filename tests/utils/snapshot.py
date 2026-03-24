# tests/utils/snapshot.py


# tests/utils/snapshot.py
from tests.utils.renderers import register_default_renderers
from tests.utils.snapshot_presets import STRUCTURE_V1
from tests.utils.tree_render_registry import registry
from tests.utils.tree_serializer import serialize_tree

# garante que os renderers estão registrados
register_default_renderers()


def assert_tree_snapshot(
    view, snapshot, config=STRUCTURE_V1, name="gallery", modes=("json", "simple")
):
    tree = serialize_tree(view, config)

    for mode in modes:
        if mode == "simple":
            # 🔹 simple usa a view (por enquanto)
            output = registry.render(mode, view)
            filename = f"{name}_{mode}.txt"
        else:
            # 🔹 estrutura (fonte da verdade)
            output = registry.render(mode, tree)
            filename = f"{name}_{config.version}.json"

        snapshot.assert_match(output, filename)
