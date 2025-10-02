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

app = FastAPI()

meu_livro = {}

@app.get("/livro")
def get_livro():
    if not meu_livro:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"Livro": meu_livro}
    
@app.post("/adicionar")
def post_livro(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in meu_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        meu_livro[id_livro] = {"nome_livro": nome_livro, "autor_livro": autor_livro, "ano_livro": ano_livro}
        return {"message": "O livro foi criado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livro(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    livro = meu_livro.get(id_livro)
    if not livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    else:
        if nome_livro:
            livro["nome_livro"] = nome_livro
        if autor_livro:
            livro["autor_livro"] = autor_livro
        if ano_livro:
            livro["ano_livro"] = ano_livro
        return {"message": "As informações do livro foram atualizadas com sucesso!"}
    
@app.delete("/delete/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    else:
        del meu_livro[id_livro]

        return {"message": "Livro deletado com sucesso!"}