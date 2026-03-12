import os
import tempfile

from eralchemy2 import render_er
from litestar import Router, get
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.models import BaseDBModel


@get("/health", tags=["system"])
async def health_check(db_session: AsyncSession) -> dict[str, str]:
    await db_session.execute(text("SELECT 1"))
    return {"status": "ok", "db": "ok"}


@get("/erd.png", tags=["system"], media_type="image/png", sync_to_thread=True)
def erd_diagram() -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp_path = f.name
    render_er(BaseDBModel.metadata, tmp_path)
    png = open(tmp_path, "rb").read()
    os.unlink(tmp_path)
    return png


system_router = Router(
    path="/",
    route_handlers=[health_check, erd_diagram],
    tags=["system"],
)
