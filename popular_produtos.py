from pymongo import MongoClient
import random

# Conectar ao MongoDB local
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["estoque"]
colecao = db["produtos"]

# Apagar todos os produtos anteriores
colecao.delete_many({})

# Dados por categoria
categorias = {
    "Utensílio Doméstico": [
        "Jogo de Panelas", "Garrafa Térmica", "Espremedor de Frutas", "Conjunto de Copos", "Sanduicheira",
        "Liquidificador", "Cafeteira Elétrica", "Tábua de Corte", "Ralador", "Conjunto de Facas"
    ],
    "Brinquedos": [
        "Carrinho Controle Remoto", "Boneca Interativa", "Blocos de Montar", "Pião com Luz", "Jogo de Memória",
        "Dinossauro Robô", "Kit de Pintura", "Patinete Infantil", "Quebra-Cabeça 100 peças", "Massinha Colorida"
    ],
    "Esportes": [
        "Bola de Futebol", "Bola de Vôlei", "Raquete de Tênis", "Patins In-Line", "Capacete de Ciclismo",
        "Bicicleta Aro 20", "Luvas de Boxe", "Colchonete para Yoga", "Corda de Pular", "Camisa Esportiva"
    ],
    "Material Escolar": [
        "Caderno Universitário", "Estojo Escolar", "Mochila com Rodinhas", "Lápis de Cor", "Canetinha Hidrocor",
        "Marca-texto", "Apontador com Depósito", "Agenda Estudantil", "Papel Sulfite 100fl", "Compasso Escolar"
    ]
}

marcas = ["Tramontina", "Tilibra", "Faber-Castell", "Luxcel", "Play-Doh", "Lego", "Caloi", "Wilson", "Brinox", "Multilaser"]
cores = ["Vermelho", "Azul", "Preto", "Rosa", "Verde", "Amarelo", "Roxo", "Branco"]
modelos = ["Clássico", "Deluxe", "Premium", "Edição Especial", "Compacto"]

produtos = []
sku_id = 1

# Gerar 50 produtos únicos
while len(produtos) < 50:
    categoria = random.choice(list(categorias.keys()))
    base_titulo = random.choice(categorias[categoria])
    marca = random.choice(marcas)
    cor = random.choice(cores)
    modelo = random.choice(modelos)

    # Gera título único
    titulo = f"{base_titulo} {modelo} - {cor}"

    produto = {
        "SKU": f"PROD{sku_id:05}",
        "Título": titulo,
        "Preço": round(random.uniform(15.0, 300.0), 2),
        "Categoria_produto": categoria,
        "Qtd_estoque": random.randint(10, 100),
        "Marca": marca,
        "Variante": [
            {"Nome": "Cor", "Opção": cor},
            {"Nome": "Modelo", "Opção": modelo}
        ]
    }

    produtos.append(produto)
    sku_id += 1

# Inserir no MongoDB
colecao.insert_many(produtos)

print("✅ 50 produtos únicos inseridos com sucesso.")

