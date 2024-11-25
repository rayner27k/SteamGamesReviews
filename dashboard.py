import pandas as pd
from pymongo import MongoClient
import plotly.express as px
import os
import glob

# Limpar arquivos HTML gerados anteriormente
for file in glob.glob("*.html"):
    os.remove(file)
print("Arquivos HTML anteriores removidos.")

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["SteamGames"]

# Carregar subconjuntos representativos dos dados
print("Carregando dados do MongoDB...")

# Jogos: trazer no máximo 10.000 registros
print("Carregando dados da coleção de games...")
games_df = pd.DataFrame(list(db.games.find()))
# Usuários: trazer no máximo 50.000 registros
print("Carregando dados da coleção de users...")
users_df = pd.DataFrame(list(db.users.find().limit(50000)))
# Reviews: trazer no máximo 50.000 registros (foco nos mais recentes)
print("Carregando dados da coleção de reviews...")
reviews_df = pd.DataFrame(list(db.reviews.find().sort("dt_review", -1).limit(50000)))

print("Dados carregados com sucesso!")

# Remover a coluna "_id" adicionada automaticamente pelo MongoDB
games_df.drop(columns=["_id"], inplace=True, errors="ignore")
users_df.drop(columns=["_id"], inplace=True, errors="ignore")
reviews_df.drop(columns=["_id"], inplace=True, errors="ignore")

# 1. Top 10 Jogos com Mais Reviews
top_reviews = games_df.nlargest(10, "qtd_reviews_usuarios")
fig1 = px.bar(
    top_reviews,
    x="titulo",
    y="qtd_reviews_usuarios",
    title="Top 10 Jogos com Mais Reviews",
    labels={"titulo": "Título do Jogo", "qtd_reviews_usuarios": "Quantidade de Reviews"},
    text="qtd_reviews_usuarios",
    color="titulo"
)
fig1.write_html("fig1_top_reviews.html")

# 2. Top 10 Jogos com Menores Taxas de Avaliação Positiva
filtered_games = games_df[games_df["taxa_avaliacao_pstv"] > 0]
low_positive = filtered_games.nsmallest(10, "taxa_avaliacao_pstv")
fig2 = px.bar(
    low_positive,
    x="titulo",
    y="taxa_avaliacao_pstv",
    title="Top 10 Jogos com Menores Taxas de Avaliação Positiva",
    labels={"titulo": "Título do Jogo", "taxa_avaliacao_pstv": "Taxa de Avaliação Positiva (%)"},
    text="taxa_avaliacao_pstv",
    color="titulo"
)
fig2.write_html("fig2_low_positive.html")

# 3. Compatibilidade de Jogos por Plataforma
platform_counts = games_df[["windows", "mac", "linux", "steam_deck"]].sum()
fig3 = px.bar(
    x=platform_counts.index,
    y=platform_counts.values,
    title="Compatibilidade de Jogos por Plataforma",
    labels={"x": "Plataforma", "y": "Quantidade de Jogos"},
    color=platform_counts.index
)
fig3.write_html("fig3_platform_compatibility.html")

# 4. Distribuição de Lançamentos por Ano
games_df["ano_lancamento"] = pd.to_datetime(games_df["dt_lancamento"], errors="coerce").dt.year
release_counts = games_df["ano_lancamento"].value_counts().sort_index()
fig4 = px.line(
    x=release_counts.index,
    y=release_counts.values,
    title="Distribuição de Lançamentos por Ano",
    labels={"x": "Ano de Lançamento", "y": "Quantidade de Jogos Lançados"}
)
fig4.write_html("fig4_release_by_year.html")

# 5. Top 10 Jogos Mais Recomendados
recommendations_count = reviews_df[reviews_df["e_recomendado"] == True]["id_jogo"].value_counts().head(10)
top_recommended_games = games_df[games_df["id_jogo"].isin(recommendations_count.index)]
top_recommended_games["qtd_recomendacoes"] = recommendations_count.values
fig5 = px.bar(
    top_recommended_games,
    x="titulo",
    y="qtd_recomendacoes",
    title="Top 10 Jogos Mais Recomendados",
    labels={"titulo": "Título do Jogo", "qtd_recomendacoes": "Quantidade de Recomendações"},
    text="qtd_recomendacoes",
    color="titulo"
)
fig5.write_html("fig5_top_recommendations.html")

# 6. Distribuição de Preços dos Jogos
price_counts = games_df["preco_final"].value_counts().sort_index()
fig_price = px.line(
    x=price_counts.index,
    y=price_counts.values,
    title="Distribuição de Preços dos Jogos",
    labels={"x": "Preço Final (em dólares)", "y": "Quantidade de Jogos"}
)
fig_price.write_html("fig6_price_distribution.html")

# 7. Correlação entre Avaliação Positiva e Número de Reviews
fig_corr = px.scatter(
    games_df,
    x="qtd_reviews_usuarios",
    y="taxa_avaliacao_pstv",
    title="Correlação entre Avaliação Positiva e Número de Reviews",
    labels={
        "qtd_reviews_usuarios": "Quantidade de Reviews",
        "taxa_avaliacao_pstv": "Taxa de Avaliação Positiva (%)"
    },
    color="avaliacao_geral",
    hover_data=["titulo"]
)
fig_corr.write_html("fig7_correlation_reviews.html")

# Converter os meses para nomes de meses
month_mapping = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# 8. Lançamentos de Jogos ao Longo do Ano
games_df["mes_lancamento"] = pd.to_datetime(games_df["dt_lancamento"], errors="coerce").dt.month
games_df["mes_lancamento_nome"] = games_df["mes_lancamento"].map(month_mapping)
monthly_launches = (
    games_df["mes_lancamento_nome"]
    .value_counts()
    .reindex(list(month_mapping.values()), fill_value=0)
)
fig_launch_timeline = px.line(
    x=monthly_launches.index,
    y=monthly_launches.values,
    title="Lançamentos de Jogos ao Longo do Ano",
    labels={"x": "Mês do Ano", "y": "Quantidade de Jogos"}
)
fig_launch_timeline.write_html("fig8_monthly_launches.html")

print("Gráficos salvos como arquivos HTML.")

# 9. Média de Reviews por Usuário
avg_reviews = users_df["qtd_reviews"].mean()
print(f"Média de Reviews por Usuário: {avg_reviews:.2f}")

# 10. Média de Quantidade de Jogos por Usuário
avg_games = users_df["qtd_jogos"].mean()
print(f"Média de Jogos por Usuário: {avg_games:.2f}")

