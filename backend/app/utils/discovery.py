"""Auto-discovery utility for importing Python modules by filename pattern.

Used to trigger decorator-based registration (e.g., @task) at startup without
requiring explicit imports in factory.py or index.py.
"""

import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def discover_and_import(filenames: list[str], base_path: str = "app") -> None:
    """Find and import all modules matching the given filenames under base_path.

    Args:
        filenames: List of filenames to search for (e.g., ["tasks.py"]).
        base_path: Root package directory to search under (e.g., "app").
    """
    base = Path(base_path)
    for filename in filenames:
        for path in sorted(base.rglob(filename)):
            # Convert filesystem path to dotted module name
            module_name = ".".join(path.with_suffix("").parts)
            try:
                importlib.import_module(module_name)
                logger.debug("Discovered and imported module: %s", module_name)
            except Exception:
                logger.exception("Failed to import discovered module: %s", module_name)
