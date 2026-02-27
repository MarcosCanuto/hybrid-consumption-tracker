from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base

# Garante que as tabelas do banco de dados estão sincronizadas com o SQLAlchemy
Base.metadata.create_all(bind=engine)

# Inicia o aplicativo FastAPI
app = FastAPI(
    title="Média Real API",
    description="API para registro e cálculo de consumo de veículos híbridos",
    version="0.1.0"
)

# Configura o CORS para permitir requisições do frontend (ajuste a origem conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de teste simples para sabermos se o servidor está online
@app.get("/")
def root():
    return {"status": "ok", "message": "MédiaReal API funcionando!"}