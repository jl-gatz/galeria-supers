from pathlib import Path, PurePosixPath


def themed_portrait_src(src: str | Path | None) -> str | None:
    if src is None:
        return None

    path = PurePosixPath(str(src).replace("\\", "/"))
    return path.as_posix()
