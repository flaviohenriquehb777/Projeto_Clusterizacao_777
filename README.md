# Amazon Product Intelligence: Pricing, Ratings & Market Segmentation

<p align="center">
  <b>Portfolio project</b> combining <b>pricing</b>, <b>discounts</b>, <b>ratings</b>, <b>PSI ranking</b>, <b>K-Means segmentation</b>, and <b>review sentiment</b> — delivered as a <b>live interactive dashboard</b>.
</p>

<p align="center">
  <a href="https://flaviohenriquehb777.github.io/Amazon_Product_Clustering/">
    <img alt="Open Live Dashboard" src="https://img.shields.io/badge/Open%20Live%20Dashboard-6366f1?style=for-the-badge&logo=github&logoColor=white">
  </a>
  <a href="amazon-product-intelligence/reports/business_questions_report.pdf">
    <img alt="Business Report PDF" src="https://img.shields.io/badge/Business%20Report-PDF-111827?style=for-the-badge">
  </a>
  <a href="https://github.com/flaviohenriquehb777/Amazon_Product_Clustering/releases">
    <img alt="Releases" src="https://img.shields.io/badge/Releases-GitHub-0b1220?style=for-the-badge&logo=github&logoColor=white">
  </a>
</p>

<p align="center">
  <a href="https://flaviohenriquehb777.github.io/Amazon_Product_Clustering/">
    <img src="amazon-product-intelligence/reports/figures/dashboard_preview.png" alt="Dashboard Preview (click to open)" width="100%"/>
  </a>
</p>

[![Release](https://img.shields.io/github/v/release/flaviohenriquehb777/Amazon_Product_Clustering?display_name=tag&sort=semver)](https://github.com/flaviohenriquehb777/Amazon_Product_Clustering/releases)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-222?logo=github&logoColor=white)](https://flaviohenriquehb777.github.io/Amazon_Product_Clustering/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)

## <a id="sumario"></a> Sumário Clicável
- [Visão Geral do Modelo](#visao-geral)
- [Objetivos da Análise](#objetivos)
- [Estrutura do Modelo](#estrutura)
- [Base de Dados](#base-de-dados)
- [Metodologia (PSI + K-Means)](#metodologia)
- [Resultados Chave](#resultados)
- [Dashboard (HTML)](#dashboard)
- [Tecnologias Utilizadas](#tecnologias)
- [Instalação e Uso](#instalacao)
- [Publicação no GitHub Pages](#github-pages)
- [Licença](#licenca)
- [Contato](#contato)

## <a id="visao-geral"></a> Visão Geral do Modelo
Este repositório contém um projeto completo de Analytics com base em um dataset de produtos da Amazon India, cobrindo:
- Qualidade/completude de dados e distribuição por categoria
- Análise de preços e descontos
- Avaliações e engajamento (rating × volume de reviews)
- Ranking de produtos por um índice proprietário (PSI — Product Score Index)
- Segmentação com K-Means (Elbow + Silhouette) e artifact do pipeline
- Análise de sentimento em reviews (texto) e comparação com rating numérico
- Dashboard interativo em HTML (Plotly + DataTables) funcionando offline e via GitHub Pages
- Relatório final com respostas quantitativas e recomendações

## <a id="objetivos"></a> Objetivos da Análise
- Identificar onde estão os maiores descontos e se eles se relacionam com rating/engajamento
- Encontrar líderes (alto rating + alto volume), “hidden gems” e “produtos problemáticos populares”
- Construir um ranking robusto (PSI) combinando rating, volume de reviews e desconto
- Segmentar produtos em clusters acionáveis para estratégia de preço, sortimento e marketing
- Explorar sentimento em reviews e divergências entre texto e nota numérica

## <a id="estrutura"></a> Estrutura do Modelo
```
Amazon_Product_Clustering/
├── amazon-product-intelligence/
│   ├── data/
│   │   └── processed/
│   ├── notebooks/
│   │   ├── clean/
│   │   └── src/
│   ├── notebooks_executed/
│   ├── reports/
│   │   ├── figures/
│   │   └── models/
│   └── dashboard/
│       └── index.html
├── docs/
│   ├── index.html
│   └── favicon.ico
└── README.md
```

## <a id="base-de-dados"></a> Base de Dados
- Fonte: dataset com ~1.4k produtos da Amazon India
- Colunas principais: `product_id`, `product_name`, `category`, preços (atual e com desconto), `discount_percentage`, `rating`, `rating_count`, reviews (`review_title`, `review_content`), links (`img_link`, `product_link`)
- Local esperado (não versionado): `amazon-product-intelligence/data/raw/dados_amazon.csv`

## <a id="metodologia"></a> Metodologia (PSI + K-Means)
- PSI (Product Score Index):
  - Combina `rating`, `log(rating_count)` e `discount_percentage` com pesos configuráveis
  - Normalização + escala 0–100 para comparabilidade entre produtos
- Segmentação (K-Means):
  - Pipeline: imputação → padronização → K-Means
  - Seleção de k com Elbow + Silhouette
  - Export do pipeline em artifact para reuso
- Sentimento:
  - Score de sentimento em `review_title` + `review_content` e comparação com o `rating`

## <a id="resultados"></a> Resultados Chave
- O dashboard consolida KPIs e permite filtrar toda a análise por categoria principal
- PSI destaca produtos com combinação de alta avaliação, alto volume e desconto competitivo
- Segmentos (clusters) permitem diferenciar estratégias: premium, desconto agressivo, “misto” e budget
- A análise de sentimento ajuda a explicar divergências entre texto do review e nota numérica
- Catálogo interativo permite explorar produtos com imagem, links e exportação CSV

## <a id="dashboard"></a> Dashboard (HTML)
- GitHub Pages (online): https://flaviohenriquehb777.github.io/Amazon_Product_Clustering/
- Offline (abrir no browser): `amazon-product-intelligence/dashboard/index.html`
- Publicação do Pages: `docs/index.html` (dados embutidos em Base64, sem depender de servidor)

## <a id="tecnologias"></a> Tecnologias Utilizadas
- Python (pandas, numpy, scikit-learn)
- Jupyter Notebooks
- Plotly (visualizações interativas)
- DataTables (tabelas com busca/ordenação/paginação)
- HTML/CSS/JavaScript (dashboard standalone)

## <a id="instalacao"></a> Instalação e Uso
1. Acesse a pasta do projeto:
   ```bash
   cd amazon-product-intelligence
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Coloque o dataset em:
   - `data/raw/dados_amazon.csv`
4. Execute os notebooks em ordem (01 → 07) em `notebooks/clean/` ou utilize `notebooks_executed/` como referência.
5. Abra o dashboard:
   - `dashboard/index.html`

## <a id="github-pages"></a> Publicação no GitHub Pages
- O projeto publica o dashboard via GitHub Pages usando a pasta `docs/` na branch `main`
- Arquivos publicados: `docs/index.html` e `docs/favicon.ico`

## <a id="licenca"></a> Licença
MIT (ver [LICENSE.md](LICENSE.md)).

## <a id="contato"></a> Contato
- Nome: Flávio Henrique Barbosa
- LinkedIn: https://linkedin.com/in/fl%C3%A1vio-henrique-barbosa-38465938
- Email: flaviohenriquehb777@outlook.com
