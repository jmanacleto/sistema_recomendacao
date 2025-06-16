from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import os

from app.data import carregar_dados
from app.model import RecomendadorNetflix

# Criação da API
app = FastAPI(title="Recomendador Netflix")

# Monta a pasta 'static' para servir arquivos como HTML, CSS, JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Redireciona a raiz "/" para a interface visual
@app.get("/")
def root():
    return RedirectResponse(url="/frontend")

# Endpoint para servir o HTML
@app.get("/frontend")
def get_frontend():
    return FileResponse(os.path.join("static", "index.html"))

# Carrega os dados e inicializa o modelo
df = carregar_dados()
modelo = RecomendadorNetflix(df)

# Endpoint principal da API de recomendação
@app.get("/recomendar/{titulo}")
def recomendar(titulo: str):
    recomendacoes = modelo.recomendar(titulo)
    if not recomendacoes:
        raise HTTPException(status_code=404, detail="Título não encontrado.")
    return {"recomendacoes": recomendacoes}