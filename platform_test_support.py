from __future__ import annotations

import importlib.util
from functools import lru_cache
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parent


@lru_cache
def client_for(slug: str) -> TestClient:
    path = ROOT / "modules" / slug / "main.py"
    spec = importlib.util.spec_from_file_location(f"all_in_one_{slug}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Modulo indisponivel: {slug}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return TestClient(module.app)
