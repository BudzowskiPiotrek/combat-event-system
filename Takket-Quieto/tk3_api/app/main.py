from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.db import engine, Base
from .routers import players_router, tournaments_router, matches_router


app = FastAPI(
    title="Takket-Quieto API",
    description="API REST para el proyecto Takket-Quieto",
    version="0.1.0"
)

# Configurar CORS
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(players_router.router)
app.include_router(tournaments_router.router)
app.include_router(matches_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Takket-Quieto API"}
