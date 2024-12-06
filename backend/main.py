from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os

# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/biblioteca") 
    return await asyncpg.connect(DATABASE_URL)

# Inicializar a aplicação FastAPI
app = FastAPI()


# Aicionar novos itens
class Livro(BaseModel):
    id: Optional[int] = None
    titulo: str
    autor: str
    ano: int
    genero: str
    quantidade: int

class Emprestimo(BaseModel):
    id_livro: int
    nome_usuario: str


# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

# Função para verificar se o livro já existe
async def verificar_livro_existente(titulo: str, autor: str, conn: asyncpg.Connection):
    try:
        query = "SELECT * FROM livros WHERE LOWER(titulo) = LOWER($1) AND LOWER(autor) = LOWER($2)"
        result = await conn.fetchval(query, titulo, autor)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se o livro existe: {str(e)}")
    
# Função para gerar um novo ID de empréstimo
async def gerar_id_emprestimo(conn: asyncpg.Connection):
    query = "SELECT nextval('empresas_id_emprestimo_seq')"  # Ajuste de acordo com o seu banco
    return await conn.fetchval(query)
    

# Adicionar um novo livro
@app.post("/api/v1/livros/", status_code=201)
async def adicionar_livro(livro: Livro):
    conn = await get_database()
    if await verificar_livro_existente(livro.titulo, livro.autor, conn):
        raise HTTPException(status_code=400, detail="Livro já cadastrado")
    
    try:
        query = """
            INSERT INTO livros (titulo, autor, ano, genero, quantidade) 
            VALUES ($1, $2, $3, $4, $5)
        """
        async with conn.transaction():
            # Certifique-se de passar todos os campos, incluindo 'ano'
            await conn.execute(query, livro.titulo, livro.autor, livro.ano, livro.genero, livro.quantidade)
        
        return {"message": "Livro cadastrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar um novo livro: {str(e)}")
    finally:
        await conn.close()


# Listar todos os itens
@app.get("/api/v1/livros/", response_model=List[Livro])
async def listar_livros():
    conn = await get_database()
    try:
        query = "SELECT * FROM livros"
        rows = await conn.fetch(query)
        livros = [dict(row) for row in rows]
        return livros
    finally:
        await conn.close()

# Buscar livro por título ou autor
@app.get("/api/v1/livros/busca/")
async def buscar_livro(titulo: Optional[str] = None, autor: Optional[str] = None):
    conn = await get_database()
    try:
        query = "SELECT * FROM livros WHERE LOWER(titulo) LIKE LOWER($1) OR LOWER(autor) LIKE LOWER($2)"
        rows = await conn.fetch(query, f"%{titulo}%", f"%{autor}%")
        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")
        return [dict(row) for row in rows]
    finally:
        await conn.close()

# Atualizar um livro existente
@app.put("/api/v1/livros/{livro_id}", response_model=Livro)
async def atualizar_livro(livro_id: int, livro: Livro):
    conn = await get_database()
    try:
        
        query_verificar = "SELECT * FROM livros WHERE id = $1"
        livro_existente = await conn.fetchrow(query_verificar, livro_id)
        
        if not livro_existente:
            raise HTTPException(status_code=404, detail="Livro não encontrado")

        query_atualizar = """
            UPDATE livros 
            SET titulo = $1, autor = $2, ano = $3, genero = $4, quantidade = $5
            WHERE id = $6
            RETURNING *;
        """
        updated_row = await conn.fetchrow(query_atualizar, livro.titulo, livro.autor, livro.ano, livro.genero, livro.quantidade, livro_id)

        return dict(updated_row)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar livro: {str(e)}")
    finally:
        await conn.close()


# Remover um item pelo ID
@app.delete("/api/v1/livros/{livro_id}", status_code=204)
async def excluir_livro(livro_id: int):
    conn = await get_database()
    try:
        query_verificar = "SELECT * FROM livros WHERE id = $1"
        livro_existente = await conn.fetchrow(query_verificar, livro_id)

        if not livro_existente:
            raise HTTPException(status_code=404, detail="Livro não encontrado")

        query_excluir = "DELETE FROM livros WHERE id = $1"
        async with conn.transaction():
            await conn.execute(query_excluir, livro_id)

        return {"message": "Livro excluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir o livro: {str(e)}")
    finally:
        await conn.close()


#Emprestar um livro
@app.post("/api/v1/emprestimos/")
async def emprestar_livro(emprestimo: Emprestimo):
    conn = await get_database()
    try:
        # Verificar se o livro existe
        query_livro = "SELECT * FROM livros WHERE id = $1"
        livro = await conn.fetchrow(query_livro, emprestimo.id_livro)
        if not livro:
            raise HTTPException(status_code=404, detail="Livro não encontrado")

        # Verificar se há quantidade disponível
        if livro["quantidade"] <= 0:
            raise HTTPException(status_code=400, detail="Não há quantidade disponível para empréstimo")

        # Registrar o empréstimo
        query_emprestimo = """
            INSERT INTO emprestimos (id_livro, nome_usuario) 
            VALUES ($1, $2)
        """
        await conn.execute(query_emprestimo, emprestimo.id_livro, emprestimo.nome_usuario)

        # Atualizar a quantidade do livro
        query_atualizar_quantidade = """
            UPDATE livros SET quantidade = quantidade - 1 WHERE id = $1
        """
        await conn.execute(query_atualizar_quantidade, emprestimo.id_livro)

        return {"message": "Livro emprestado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao emprestar livro: {str(e)}")
    finally:
        await conn.close()

@app.get("/api/v1/emprestimos/", response_model=List[Emprestimo])
async def listar_emprestimos():
    conn = await get_database()
    try:
        query = "SELECT * FROM emprestimos WHERE data_devolucao IS NULL"
        rows = await conn.fetch(query)
        emprestimos = [dict(row) for row in rows]
        return emprestimos
    finally:
        await conn.close()

# Devolver um livro
@app.post("/api/v1/devolucoes/")
async def devolver_livro(emprestimo: Emprestimo):
    conn = await get_database()
    try:
        
        query_emprestimo = """
            SELECT * FROM emprestimos 
            WHERE id_livro = $1 AND nome_usuario = $2 AND data_devolucao IS NULL
        """
        registro_emprestimo = await conn.fetchrow(query_emprestimo, emprestimo.id_livro, emprestimo.nome_usuario)
        if not registro_emprestimo:
            raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou já devolvido")

        query_devolucao = """
            UPDATE emprestimos 
            SET data_devolucao = CURRENT_TIMESTAMP 
            WHERE id_livro = $1 AND nome_usuario = $2 AND data_devolucao IS NULL
        """
        await conn.execute(query_devolucao, emprestimo.id_livro, emprestimo.nome_usuario)

        
        query_atualizar_quantidade = """
            UPDATE livros SET quantidade = quantidade + 1 WHERE id = $1
        """
        await conn.execute(query_atualizar_quantidade, emprestimo.id_livro)

        return {"message": "Livro devolvido com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao devolver livro: {str(e)}")
    finally:
        await conn.close()


#Resetar o repositório de livros
@app.delete("/api/v1/livros/")
async def resetar_livros():
    init_sql = os.getenv("INIT_SQL", "/app/db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()

