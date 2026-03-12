"""Application entry point.

Model discovery auto-imports all models.py files so BaseDBModel.metadata
is fully populated before create_app() runs.
"""

from app.utils.discovery import discover_and_import

discover_and_import(["models.py", "models/**/*.py"])

from app.factory import create_app
from app.utils.configure import config

app = create_app(config=config)
