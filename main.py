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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

meu_livro = {}

class Livros(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

    
@app.get("/livro")
def get_livro():
    if not meu_livro:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"Livro": meu_livro}
    
@app.post("/adicionar")
def post_livro(id_livro: int, livro: Livros):
    if id_livro in meu_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        meu_livro[id_livro] = livro.model_dump()
        return {"message": "O livro foi criado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livro(id_livro: int, livro: Livros):
    livro_atu = meu_livro.get(id_livro)
    if not livro_atu:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    else:
        meu_livro[id_livro] = livro.model_dump()
        return {"message": "As informações do livro foram atualizadas com sucesso!"}
    
@app.delete("/delete/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    else:
        del meu_livro[id_livro]

        return {"message": "Livro deletado com sucesso!"}