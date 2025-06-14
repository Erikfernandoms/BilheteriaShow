from fastapi import FastAPI
from app.controllers.usuarios.routes import router as usuarios_router
from app.controllers.eventos.routes import router as eventos_router
from app.controllers.produtos.routes import router as produtos_router
from app.controllers.pedidos.routes import router as pedidos_router
from app.controllers.pagamentos.routes import router as pagamentos_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(title="Sistema de Bilhetagem", lifespan=lifespan)

app.include_router(usuarios_router, prefix="/usuarios", tags=["usuarios"])
app.include_router(eventos_router, prefix="/eventos", tags=["eventos"])
app.include_router(produtos_router, prefix="/produtos", tags=["produtos"])
app.include_router(pedidos_router, prefix="/pedidos", tags=["pedidos"])
app.include_router(pagamentos_router, prefix="/pagamentos", tags=["pagamentos"])