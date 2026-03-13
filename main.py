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
import redis
import json

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import asyncio

load_dotenv()

#Variaveis de ambiente
#DATABASE_URL = "sqlite:///./livros.db"
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

redis_client = redis.Redis(host="redis_cache", port=6379, db=0, decode_responses=True)

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="API de livros",
    description="API para gerenciar catálogos de livros.",
    version="1.0.0",
    contact={
        "name":"Guilherme Vital",
        "email":"guilhermev.j.santos@gmail.com"
    }
)
# Variaveis de ambiente
#MEU_USUARIO = "admin"
#MINHA_SENHA = "admin"

MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")
security = HTTPBasic()

meu_livro = {}

class LivrosDB(Base):
    __tablename__="livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer)

class Livros(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

Base.metadata.create_all(bind=engine)

async def salvar_livros_redis(id_livro: int, livro: Livros):
    #redis_client.set(f"livro:{id_livro}", json.dumps(livro.model_dump()))
    redis_client.setex(f"livro:{id_livro}", 30, json.dumps(livro.model_dump()))
    chave_pag = redis_client.keys("livro:page=*")
    if chave_pag:
        redis_client.delete(*chave_pag)


async def deletar_livros_redis(id_livro: int):
    redis_client.delete(f"livro:{id_livro}")
    chave_pag = redis_client.keys("livro:page=*")
    if chave_pag:
        redis_client.delete(*chave_pag)

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário e senha incorretos",
            headers={"WWW-Autheticate": "Basic"}
        )
    
async def chamadas_externas_1():
    await asyncio.sleep(2)
    return "https://pokeapi.co/api/v2/ability/1/"
    
async def chamadas_externas_2():
    await asyncio.sleep(2)
    return "Resultado Chamada externa 2"

async def chamadas_externas_3():
    await asyncio.sleep(2)
    return "Resultado Chamada externa 3"

@app.get("/chamadas-externas")
async def chamadas_externas():
    tarefa1 = asyncio.create_task(chamadas_externas_1())
    tarefa2 = asyncio.create_task(chamadas_externas_2())
    tarefa3 = asyncio.create_task(chamadas_externas_3())

    resultado1 = await tarefa1
    resultado2 = await tarefa2
    resultado3 = await tarefa3

    return {
        "mensagem": "Todas as chamadas nas API's foram concluidas com sucesso",
        "resultado": [resultado1, resultado2, resultado3]
    }

@app.get("/debug/redis")
def ver_livros_redis():
    chaves = redis_client.keys("livro:*")
    livros = []

    for chave in chaves:
        valor = redis_client.get(chave)
        ttl = redis_client.ttl(chave)
        if valor:
            livros.append({"chave": chave, "valor": json.loads(valor), "ttl": ttl})

    return livros



@app.get("/livros")
def get_livros(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos.")
    
    cache_key = f"livro:page={page}&limit={limit}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)
    
    livros = db.query(LivrosDB).offset((page - 1) * limit).limit(limit).all()

    if not livros:
        return {"message": "Não existe livro nenhum."}
    
    total_livros = db.query(LivrosDB).count()

    resposta = {
        "page": page,
        "limit": limit,
        "total": total_livros,
        "livros": [
            {
                "id": livro.id,
                "nome_livro": livro.nome_livro,
                "autor_livro": livro.autor_livro,
                "ano_livro": livro.ano_livro
            } for livro in livros
        ]
    }

    redis_client.setex(cache_key, 30, json.dumps(resposta))
    
    return resposta
    
    
#async def get_livro(page: int = 1, limit: int = 10, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
#    if page < 1 or limit < 1:
#        raise HTTPException(status_code=400, detail="Page ou limit inválido")
    
#    livros = db.query(LivrosDB).offset((page - 1) * limit).limit(limit).all()
    
#    if not livros:
#        return {"message": "Não existe nenhum livro."}

# =============================================================================================================================   
    #livros_ordenados = sorted(meu_livro.items(), key=lambda x: x[0])

    #start = (page - 1) * limit
    #end = start + limit

    #livros_paginados = [
    #    {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
    #    for id_livro, livro_data in livros_ordenados[start:end]
    #]

# ===============================================================================================================================

#    total_livros = db.query(LivrosDB).count()

#    return {
#        "page": page,
#        "limit": limit,
#        "total": (total_livros),
#        "livros": [{"id": livro.id, "nome_livro": livro.nome_livro, "autor_livro": livro.autor_livro, "ano_livro": livro.ano_livro} for livro in livros]
#    }
    
@app.post("/adicionar")
async def post_livro(livro: Livros, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivrosDB).filter(LivrosDB.nome_livro == livro.nome_livro, LivrosDB.autor_livro == livro.autor_livro).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe dentro do banco de dados!")
    
    novo_livro = LivrosDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    
    db.commit()
    db.refresh(novo_livro)

    await salvar_livros_redis(novo_livro.id, livro)

    return{"message": "Livro criado com sucesso"}

    #if id_livro in meu_livro:
    #    raise HTTPException(status_code=400, detail="Esse livro já existe")
    #else:
    #    meu_livro[id_livro] = livro.model_dump()
    #    return {"message": "O livro foi criado com sucesso!"}


@app.put("/atualizar/{id_livro}")
async def put_livro(id_livro: int, livro: Livros, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivrosDB).filter(LivrosDB.id == id_livro). first()
    if not db_livro:
        raise HTTPException(status_code=400, detail="Este livro não foi encontrado no banco de dados!")
    
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro

    db.commit()
    db.refresh(db_livro)

    await salvar_livros_redis(db_livro.id, livro)

    return {"message": "Livro atualizado com sucesso!"}

    #livro_atu = meu_livro.get(id_livro)
    #if not livro_atu:
    #    raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    #else:
    #    meu_livro[id_livro] = livro.model_dump()
    #    return {"message": "As informações do livro foram atualizadas com sucesso!"}
    
@app.delete("/delete/{id_livro}")
async def delete_livro(id_livro: int, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivrosDB).filter(LivrosDB.id == id_livro). first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado no banco de dados!")
    
    db.delete(db_livro)
    db.commit()

    await deletar_livros_redis(id_livro)

    return{"message": "Seu livro foi deletado com sucesso!"}

    #if id_livro not in meu_livro:
    #    raise HTTPException(status_code=404, detail="Esse livro não foi encontrado.")
    #else:
    #    del meu_livro[id_livro]

    #    return {"message": "Livro deletado com sucesso!"}