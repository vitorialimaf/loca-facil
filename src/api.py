from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus


password = quote_plus("MONGO_PASSWORD")
MONGO_URI = f"mongodb+srv://JULIA:{password}@cluster0.ehmhzlg.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
db = client["locafacil"]
collection = db["filmes"]


app = FastAPI(title="LocaFácil API")


@app.post("/filme")
def inserir_filme(filme: dict):
    if collection.find_one({"titulo": filme["titulo"]}):
        return {"mensagem": "Filme já cadastrado"}

    collection.insert_one({
        "titulo": filme["titulo"],
        "genero": filme["genero"],
        "ano": filme["ano"],
        "disponivel": True
    })

    return {"mensagem": "Filme inserido com sucesso"}

@app.post("/filmes")
def inserir_varios_filmes(filmes: list[dict]):
    collection.insert_many(filmes)
    return {
        "mensagem": "Filmes inseridos com sucesso",
        "quantidade": len(filmes)
    }

@app.get("/filmes")
def listar_filmes():
    filmes = []
    for filme in collection.find():
        filme["_id"] = str(filme["_id"])
        filmes.append(filme)
    return filmes

@app.put("/filme/{titulo}")
def atualizar_disponibilidade(titulo: str, status: bool):
    resultado = collection.update_one(
        {"titulo": titulo},
        {"$set": {"disponivel": status}}
    )

    if resultado.matched_count == 0:
        return {"mensagem": "Filme não encontrado"}

    return {"mensagem": "Disponibilidade atualizada"}

@app.delete("/filme/{titulo}")
def remover_filme(titulo: str):
    resultado = collection.delete_one({"titulo": titulo})

    if resultado.deleted_count == 0:
        return {"mensagem": "Filme não encontrado"}

    return {"mensagem": "Filme removido com sucesso"}

@app.get("/analytics/filmes-por-genero")
def filmes_por_genero():
    pipeline = [
        {
            "$group": {
                "_id": "$genero",
                "quantidade": {"$sum": 1}
            }
        }
    ]

    return list(collection.aggregate(pipeline))

@app.get("/analytics/status-filmes")
def status_filmes():
    pipeline = [
        {
            "$group": {
                "_id": "$disponivel",
                "quantidade": {"$sum": 1}
            }
        }
    ]

    return list(collection.aggregate(pipeline))
