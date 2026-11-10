from pathlib import Path
import sys


def get_base_path() -> Path:
    # Returns the base path of the app.
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parents[2]


def get_asset_path(*parts: str) -> Path:
    # Returns the path to an asset file.
    return get_base_path() / "assets" / Path(*parts)
