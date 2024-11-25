import pandas as pd
from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["SteamGames"]

# Dicionários de mapeamento de colunas
column_mappings = {
    "games": {
        "app_id": "id_jogo",
        "title": "titulo",
        "date_release": "dt_lancamento",
        "win": "windows",
        "mac": "mac",
        "linux": "linux",
        "steam_deck": "steam_deck",
        "rating": "avaliacao_geral",
        "positive_ratio": "taxa_avaliacao_pstv",
        "user_reviews": "qtd_reviews_usuarios",
        "price_final": "preco_final",
        "price_original": "preco_original",
        "discount": "pctg_desconto"
    },
    "users": {
        "user_id": "id_usuario",
        "products": "qtd_jogos",
        "reviews": "qtd_reviews"
    },
    "reviews": {
        "app_id": "id_jogo",
        "helpful": "qtd_avld_util",
        "funny": "qtd_avld_divertido",
        "date": "dt_review",
        "is_recommended": "e_recomendado",
        "hours": "horas_jogadas",
        "user_id": "id_usuario",
        "review_id": "id_review"
    }
}

# Função para renomear colunas e reorganizar, se necessário
def rename_and_reorganize_columns(data, collection_name):
    # Renomear colunas
    if collection_name in column_mappings:
        data.rename(columns=column_mappings[collection_name], inplace=True)

    # Reorganizar colunas na coleção de games
    if collection_name == "games":
        columns_order = list(data.columns)
        if "steam_deck" in columns_order and "linux" in columns_order:
            steam_deck_index = columns_order.index("steam_deck")
            linux_index = columns_order.index("linux")
            # Remove e reinsere steam_deck logo após a coluna 'linux'
            columns_order.pop(steam_deck_index)
            columns_order.insert(linux_index + 1, "steam_deck")
            data = data[columns_order]
    return data

# Função para extrair, transformar e carregar os dados
def process_and_load(file_path, collection_name):
    # Ler arquivo CSV ou Excel
    try:
        data = pd.read_csv(file_path)
    except:
        data = pd.read_excel(file_path)

    # Renomear e reorganizar as colunas
    data = rename_and_reorganize_columns(data, collection_name)

    # Limpeza básica dos dados: remove duplicados e preenche valores nulos
    data.drop_duplicates(inplace=True)
    data.fillna("N/A", inplace=True)

    # Carregar no MongoDB
    collection = db[collection_name]
    batch_size = 1000 # Tamanho do lote (Mude de acordo com a sua máquina)
    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i + batch_size].to_dict("records")
        collection.insert_many(batch)
        print(f"Lote {i // batch_size + 1} de {collection_name} carregado.")

# Arquivos e coleções
files_and_collections = {
    "data/users.csv": "users",
    "data/games.csv": "games",
    "data/recommendations.csv": "reviews"
}

# Executar ETL para cada arquivo
for file_path, collection_name in files_and_collections.items():
    process_and_load(file_path, collection_name)

print("ETL concluído com sucesso!")
