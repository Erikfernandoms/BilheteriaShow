from fastapi import FastAPI
from app.controllers.usuarios.routes import router as usuarios_router
from app.controllers.eventos.routes import router as eventos_router
#from app.api.produtos.routes import router as produtos_router
#from app.api.pedidos.routes import router as pedidos_router



app = FastAPI(title="Sistema de Bilhetagem")





app.include_router(usuarios_router, prefix="/usuarios", tags=["usuarios"])
app.include_router(eventos_router, prefix="/eventos", tags=["eventos"])
#app.include_router(produtos_router, prefix="/produtos", tags=["produtos"])
