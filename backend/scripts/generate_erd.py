#!/usr/bin/env python3
"""Generate an ERD diagram for the database schema.

Requires graphviz and eralchemy2 to be installed:
    brew install graphviz
    uv run --with eralchemy2 python scripts/generate_erd.py [output.png]
"""

import sys

sys.path.insert(0, ".")

import app.index  # triggers model discovery so metadata is populated

output = sys.argv[1] if len(sys.argv) > 1 else "erd.png"

from eralchemy2 import render_er  # type: ignore[import-untyped]

from app.base.models import BaseDBModel

render_er(BaseDBModel.metadata, output)
print(f"ERD written to {output}")
