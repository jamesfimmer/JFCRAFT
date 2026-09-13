"""Compatibility entry point: use the unified launcher."""
from jfcraft_core import Installer, load_manifest

if __name__ == "__main__":
    from launcher_ui import startup
    startup()
