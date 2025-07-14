# data_loader.py
from pymongo import MongoClient
import pandas as pd

def carregar_dados_mongo():
    # Conecta ao MongoDB local
    uri = "mongodb://localhost:27017/"
    cliente = MongoClient(uri)

    # Define nome da base e da coleção
    db = cliente["estoque"]
    colecao = db["produtos"]

    # Busca os dados e converte para DataFrame
    dados = list(colecao.find({}, {'_id': 0}))  # Exclui o campo _id
    df = pd.DataFrame(dados)    

    return df

def carregar_movimentacoes_estoque():
    cliente = MongoClient("mongodb://localhost:27017/")
    db = cliente["estoque"]
    colecao = db["estoque"]
    dados = list(colecao.find({}, {"_id": 0}))  # Exclui o _id
    return pd.DataFrame(dados)
