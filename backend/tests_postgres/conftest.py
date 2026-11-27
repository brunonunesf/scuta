"""Integração real, em schema descartável exclusivo; nunca reutiliza o schema public.

Executar separadamente: TEST_POSTGRES_URL=... uv run pytest tests_postgres -v
"""
import os
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture(scope="session")
def app_postgres():
    endereco = os.getenv("TEST_POSTGRES_URL")
    if not endereco:
        pytest.skip("Defina TEST_POSTGRES_URL para executar a integração PostgreSQL")
    url = make_url(endereco).set(drivername="postgresql+psycopg")
    schema = "scuta_test_" + uuid4().hex
    admin = create_engine(url)
    with admin.begin() as db:
        db.execute(text(f'CREATE SCHEMA "{schema}"'))
    anterior = {k: os.environ.get(k) for k in ("DATABASE_URL", "CORS_ORIGINS", "DEBUG")}
    os.environ["DATABASE_URL"] = url.update_query_dict({"options": f"-csearch_path={schema}"}).render_as_string(hide_password=False)
    os.environ["CORS_ORIGINS"] = "https://scuta-app.vercel.app,https://miniprojeto3-musica.vercel.app"
    os.environ["DEBUG"] = "false"
    try:
        # Os testes SQLite configuram outro engine; rode as suítes em processos separados.
        if "app.db" in sys.modules:
            raise RuntimeError("Execute tests_postgres separadamente da suíte SQLite")
        from app.db import engine
        from app.main import app
        yield app
        engine.dispose()
    finally:
        for chave, valor in anterior.items():
            if valor is None:
                os.environ.pop(chave, None)
            else:
                os.environ[chave] = valor
        with admin.begin() as db:
            db.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()
