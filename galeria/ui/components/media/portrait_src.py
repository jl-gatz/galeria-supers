from pathlib import Path, PurePosixPath


def themed_portrait_src(src: str | Path | None) -> str | None:
    if src is None:
        return None

    path = PurePosixPath(str(src).replace("\\", "/"))

    if path.suffix != ".png" or not path.name.endswith("__transp.png"):
        return path.as_posix()

    gray_name = path.name.replace("__transp.png", "__gray.png")

    return (path.parent / "grayscale" / gray_name).as_posix()
