from __future__ import annotations

import sys
from pathlib import Path


def _prepare_imports() -> None:
    """Добавить корень проекта в sys.path для корректных импортов."""
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[2]

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def main() -> None:
    """Точка входа в консольное приложение."""
    _prepare_imports()

    from src.lab07.app import ShopApp
    from src.lab07.cli import ShopCLI

    app = ShopApp()
    cli = ShopCLI(app)
    cli.run()


if __name__ == '__main__':
    main()