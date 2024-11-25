from fastapi import FastAPI
from app.routes.api import api_router

app = FastAPI(title="Qwizzo AI Backend")

# Rota principal para teste
@app.get("/")
def root():
    return {"message": "Bem-vindo ao backend do Qwizzo AI!"}

# Incluindo rotas de API
app.include_router(api_router)
