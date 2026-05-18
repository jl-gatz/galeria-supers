from types import SimpleNamespace

from galeria.ui.components.media.themed_logo import ThemedLogo, resolve_logo_src
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def test_resolve_logo_src_returns_themed_logo_when_file_exists(tmp_path):
    logos_dir = tmp_path / "logos"
    themed_dir = logos_dir / "ccuec_era"
    themed_dir.mkdir(parents=True)
    (themed_dir / "logo-detic-4x.png").touch()
    (logos_dir / "logo-detic-4x.png").touch()

    assert (
        resolve_logo_src("ccuec_era", "logo-detic-4x.png", logos_dir=logos_dir)
        == "images/logos/ccuec_era/logo-detic-4x.png"
    )


def test_resolve_logo_src_returns_fallback_when_themed_logo_is_missing(tmp_path):
    logos_dir = tmp_path / "logos"
    logos_dir.mkdir()
    (logos_dir / "logo-detic-4x.png").touch()

    assert (
        resolve_logo_src("greenish", "logo-detic-4x.png", logos_dir=logos_dir)
        == "images/logos/logo-detic-4x.png"
    )


def test_themed_logo_updates_src_when_theme_changes(monkeypatch, tmp_path):
    logos_dir = tmp_path / "logos"
    themed_dir = logos_dir / "ccuec_era"
    themed_dir.mkdir(parents=True)
    (themed_dir / "logo-detic-4x.png").touch()
    (logos_dir / "logo-detic-4x.png").touch()

    monkeypatch.setattr(
        "galeria.ui.components.media.themed_logo.LOGOS_DIR",
        logos_dir,
    )

    theme = FakeTheme()
    theme.id = "missing_theme"
    manager = FakeThemeManager(theme)
    logo = ThemedLogo(
        theme_manager=manager,
        filename="logo-detic-4x.png",
    )

    assert logo.src == "images/logos/logo-detic-4x.png"

    logo._apply_theme(SimpleNamespace(id="ccuec_era"))

    assert logo.src == "images/logos/ccuec_era/logo-detic-4x.png"
