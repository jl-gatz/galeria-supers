# tests/utils/snapshot_presets.py

from .snapshot_config import SnapshotConfig
from .types import JsonValue


def mask_image(_: JsonValue) -> JsonValue:
    return "[IMAGE]"


# 🔹 Estrutura pura (CI padrão)
STRUCTURE_V1 = SnapshotConfig(
    version="structure@v1",
    exclude_props={"src", "key", "id"},
    ignore_types={"Spacer"},
    max_depth=5,
)


# 🔹 Semântico (equilíbrio)
SEMANTIC_V1 = SnapshotConfig(
    version="semantic@v1",
    exclude_props={"key", "id"},
    transform_values={
        "src": mask_image,
    },
)


# 🔹 Completo (debug / staging)
FULL_V1 = SnapshotConfig(
    version="full@v1",
)
