"""Crea las tablas en la base de datos.

Uso:
    .venv\\Scripts\\python.exe -m scripts.init_db

Nota: para entornos de producción se recomienda usar Alembic para migraciones.
"""

import asyncio
import selectors
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text

from app.core.config import settings
from app.core.database import Base, engine
import app.models  # noqa: F401  (registra todos los modelos)


async def init() -> None:
    print(f"Conectando a: {settings.DATABASE_URL.rsplit('@', 1)[-1]}")
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
        print("Conexión exitosa a PostgreSQL")
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas/verificadas.")


if __name__ == "__main__":
    asyncio.run(init(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()))
