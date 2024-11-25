# Steam Games Reviews Dashboard

Este projeto utiliza Python, MongoDB e Plotly para criar um pipeline ETL e gerar dashboards interativos com dados de jogos da Steam. Ele permite realizar análises visuais sobre diversos aspectos dos dados, como avaliações, compatibilidade de plataformas e distribuição de preços.

## Dataset

Os dados utilizados neste projeto foram retirados do seguinte dataset:

- [Game Recommendations on Steam](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam)

Este dataset contém informações detalhadas sobre jogos disponíveis na plataforma Steam, incluindo avaliações, preços, compatibilidade de plataformas e muito mais.

## Estrutura do Projeto

- **data/**: Contém os arquivos CSV usados como entrada para o pipeline ETL.
  - `games.csv`
  - `recommendations.csv`
  - `users.csv`
- **etl_pipeline.py**: Script de pipeline ETL que carrega os dados dos arquivos CSV para o MongoDB, realiza transformação de colunas e remove duplicatas.
- **dashboard.py**: Script que gera gráficos interativos a partir dos dados carregados no MongoDB.
- **fig\*.html**: Arquivos HTML gerados contendo gráficos interativos.

## Pré-requisitos

Certifique-se de que sua máquina atenda aos seguintes requisitos:

- Python 3.9+
- MongoDB Community Server instalado e rodando na porta padrão 27017.
- Bibliotecas Python listadas no arquivo `requirements.txt`.

## Instalação

Clone este repositório:

```bash
git clone https://github.com/rayner27k/SteamGamesReviews
cd SteamGamesReviews
code .
```

Baixe os arquivos de dados do [Dataset do Kaggle](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam), e dentro do repositório, crie uma pasta chamada `data`, traga os arquivos **CSV** do dataset para dentro dessa pasta, ficando ao final com esses arquivos dentro de `data`:

```bash
games.csv
recommendations.csv
users.csv
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate # Linux/MacOS
source venv/Scripts/activate # Bash
venv\Scripts\activate # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o MongoDB: Certifique-se de que o MongoDB está rodando na porta padrão (localhost:27017).

Carregue os dados para o MongoDB: Execute o pipeline ETL para processar os arquivos CSV e carregar os dados no MongoDB:

```bash
python etl_pipeline.py
```

## Uso

Gerar gráficos interativos: Execute o script `dashboard.py` para gerar gráficos interativos salvos em arquivos HTML:

```bash
python dashboard.py
```

Abrir os gráficos: Os gráficos gerados estarão disponíveis como arquivos HTML no diretório principal. Abra-os no navegador para visualização.

## Gráficos Gerados

- **Top 10 Jogos com Mais Reviews** (`fig1_top_reviews.html`)
- **Top 10 Jogos com Menores Taxas de Avaliação Positiva** (`fig2_low_positive.html`)
- **Compatibilidade de Jogos por Plataforma** (`fig3_platform_compatibility.html`)
- **Distribuição de Lançamentos por Ano** (`fig4_release_by_year.html`)
- **Top 10 Jogos Mais Recomendados** (`fig5_top_recommendations.html`)
- **Distribuição de Preços dos Jogos** (`fig6_price_distribution.html`)
- **Correlação entre Avaliação Positiva e Número de Reviews** (`fig7_correlation_reviews.html`)
- **Lançamentos de Jogos ao Longo do Ano** (`fig8_monthly_launches.html`)

## Sugestões de Melhorias

### Otimização para grandes volumes de dados:

- Se quiser usar as bases completas (milhões de registros), considere:
  - Um servidor dedicado para MongoDB com boa memória e armazenamento.
  - Usar agregações no MongoDB para reduzir a quantidade de dados retornados.
  - Ajustar os limites de consulta (`limit()`).

### Substituir Plotly por Dash:

- Integre os gráficos em um dashboard com Dash para visualizações centralizadas e navegação mais intuitiva.

### Uso de Dask ou PySpark:

- Para lidar com bases de dados muito grandes, bibliotecas como Dask ou PySpark podem ajudar no processamento distribuído.

### Melhorias no pipeline ETL:

- Adicionar verificações mais robustas de consistência dos dados e manipulação de exceções.

### Criar um arquivo de configuração:

- Use um arquivo `.env` para armazenar as configurações do MongoDB, como host e porta.

## Notas para Altos Volumes de Dados

### Hardware recomendado:

- Pelo menos 16 GB de RAM e um disco SSD para cargas completas.

### Otimize o MongoDB:

- Utilize índices adequados nas coleções (`id_jogo`, `id_usuario`, `dt_review`) para acelerar as consultas.

## Observações

- Os dados de games retirados do dataset, no momento do projeto, têm sua base de dados atualizada até 23 de outubro de 2023.
- Caso os hardwares da sua máquina não sejam tão bons, você talvez consiga rodar bem o código limitando a quantidade de dados em uma menor amostragem.

### Se tiver dúvidas, sugestões ou quiser contribuir, sinta-se à vontade para abrir uma issue ou pull request no repositório. 🤝
