from importlib import import_module
from pathlib import Path

SOURCE_DIR = Path("galeria/assets/images/supers")
OUTPUT_DIR = SOURCE_DIR / "grayscale"


def main():
    try:
        image_module = import_module("PIL.Image")
    except ImportError as exc:
        raise SystemExit(
            "Pillow is required to generate grayscale assets. "
            "Install it with: poetry add --group dev pillow"
        ) from exc

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for source in sorted(SOURCE_DIR.glob("*__transp.png")):
        output = OUTPUT_DIR / source.name.replace("__transp.png", "__gray.png")

        with image_module.open(source).convert("RGBA") as image:
            grayscale = image.convert("LA")
            alpha = image.getchannel("A")
            result = image_module.merge("RGBA", (*grayscale.convert("RGB").split(), alpha))
            result.save(output)

        print(f"generated {output}")


if __name__ == "__main__":
    main()
