from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb+srv://vitorialimaf2002_db_user:ibfyWoqnIQUfnzNf@cluster0.ctn9dxq.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    print("Conectado ao MongoDB Atlas com sucesso!")
except ConnectionFailure:
    print("Erro ao conectar ao MongoDB Atlas.")

db = client["locafacil"]
collection = db["filmes"]

def inserir_filme(titulo, genero, ano):
    filme = {
        "titulo": titulo,
        "genero": genero,
        "ano": ano,
        "disponivel": True
    }
    collection.insert_one(filme)
    print("Filme inserido com sucesso!")

def listar_filmes():
    print("\nLista de filmes:")
    for filme in collection.find():
        print(filme)

def atualizar_disponibilidade(titulo, status):
    resultado = collection.update_one(
        {"titulo": titulo},
        {"$set": {"disponivel": status}}
    )
    if resultado.matched_count > 0:
        print("Disponibilidade atualizada!")
    else:
        print("Filme não encontrado.")

def remover_filme(titulo):
    resultado = collection.delete_one({"titulo": titulo})
    if resultado.deleted_count > 0:
        print("Filme removido!")
    else:
        print("Filme não encontrado.")

if __name__ == "__main__":
    inserir_filme("Matrix", "Ficção Científica", 1999)
    inserir_filme("Interestelar", "Ficção Científica", 2014)
    listar_filmes()
    atualizar_disponibilidade("Matrix", False)
    remover_filme("Matrix")
    listar_filmes()
