# API de livros.

# GET, POST, PUT, DELETE

# POST - Adicionar novos livros
# GET - Buscar os dados dos livros
# PUT - Atualizar informações dos livros
# DELETE - Deletar informações dos livros

# CRUD
# Create
# Read
# Update
# Delete

# Para rodar o FastAPI no terminal: fastapi dev (e o nome do arquivo .py).

#Documentação Swagger -> Documentar os endpoints das aplicações (Das API)
#Documentação Swagger nesse endpoint -> http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

app = FastAPI(
    title="API de livros",
    description="API para gerenciar catálogos de livros.",
    version="1.0.0",
    contact={
        "name":"Guilherme Vital",
        "email":"guilhermev.j.santos@gmail.com"
    }
)

MEU_USUARIO = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()

meu_livro = {}

class Livros(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int   

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário e senha incorretos",
            headers={"WWW-Autheticate": "Basic"}
        )
    
@app.get("/livro")
def get_livro(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit inválido")
    
    if not meu_livro:
        return {"message": "Não existe nenhum livro."}
    
    livros_ordenados = sorted(meu_livro.items(), key=lambda x: x[0])

    start = (page - 1) * limit
    end = start + limit

    livros_paginados = [
        {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
        for id_livro, livro_data in livros_ordenados[start:end]
    ]

    return {
        "page": page,
        "limit": limit,
        "total": len(meu_livro),
        "livros": livros_paginados
    }
    
@app.post("/adicionar")
def post_livro(id_livro: int, livro: Livros, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro in meu_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        meu_livro[id_livro] = livro.model_dump()
        return {"message": "O livro foi criado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livro(id_livro: int, livro: Livros, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    livro_atu = meu_livro.get(id_livro)
    if not livro_atu:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    else:
        meu_livro[id_livro] = livro.model_dump()
        return {"message": "As informações do livro foram atualizadas com sucesso!"}
    
@app.delete("/delete/{id_livro}")
def delete_livro(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro not in meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    else:
        del meu_livro[id_livro]

        return {"message": "Livro deletado com sucesso!"}