"""Arranca el servidor de desarrollo con el event loop correcto para Windows.

Uso:
    .venv\\Scripts\\python.exe run.py
"""

import asyncio
import selectors
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn


def _selector_loop():
    return asyncio.SelectorEventLoop(selectors.SelectSelector())


async def _serve() -> None:
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(_serve(), loop_factory=_selector_loop)
