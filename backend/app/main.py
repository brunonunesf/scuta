from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from app.config import origens_permitidas

from app.core.contadores import contador_iniciais
from app.db import Base, SessionLocal, atualizar_esquema_antigo, engine
from app.models.user import User
from app.routers import (
    arvores,
    auth,
    bibliotecas,
    comentarios,
    curtidas,
    descobrir,
    feed,
    follows,
    musicas,
    posts,
    reescutas,
    users,
)
from app.services import arvores as servico_arvores
from app.services import musicas as servico_musicas
from app.services import reputacao as servico_reputacao


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    atualizar_esquema_antigo()  # banco criado antes de uma entrega ganha as colunas novas
    # Reconstrói as estruturas do core/ a partir do banco (memória zera a cada
    # restart — inclusive no --reload; ver core/README.md).
    with SessionLocal() as db:
        servico_musicas.importar_catalogo(db)  # catálogo curado; repetir é seguro
        usernames = list(db.scalars(select(User.username)))
        servico_arvores.tentar_reconstruir(db)  # floresta de reviews; dado inconsistente não impede a subida
        servico_reputacao.sincronizar_eventos(db)  # curtidas e derivadas que já existem (seed, banco antigo)
        servico_reputacao.recalcular(db)  # só libera totais após reconstruir árvore e eventos
    contador_iniciais.reconstruir(usernames)
    yield


app = FastAPI(title="Rede Social da Trilha", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health():
    try:
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(status_code=503, content={"status": "unavailable"})
    return {"status": "ok"}


# 1 linha por feature — registre o seu router aqui.
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(bibliotecas.router)
app.include_router(follows.router)
app.include_router(feed.router)
app.include_router(descobrir.router)
app.include_router(musicas.router)
app.include_router(posts.router)
app.include_router(curtidas.router)
app.include_router(comentarios.router)
app.include_router(reescutas.router)
app.include_router(arvores.router)
