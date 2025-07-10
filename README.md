# Projeto de Clusterização de Produtos da Amazon

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Aplicação de Machine Learning Não Supervisionado para segmentação de produtos da Amazon em clusters, visando insights estratégicos para marketing e otimização de catálogos.**

## Sumário
- [Descrição do Projeto](#descrição-do-projeto)
- [Demonstração](#demonstração)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Geração de Arquivos Essenciais (Powershell)](#geração-de-arquivos-essenciais-powershell)
- [Contribuições](#contribuições)
- [Contato](#contato)

## Descrição do Projeto

O core deste projeto reside na identificação do número ideal de clusters (`K`) e na aplicação do algoritmo K-Means para agrupar produtos da Amazon. A análise é complementada pela redução de dimensionalidade com PCA para visualização em 2D e a automatização da geração de relatórios executivos em PDF. O objetivo final é transformar dados brutos em informações acionáveis, fornecendo insights estratégicos para otimização de campanhas de marketing, organização de catálogos e personalização de recomendações.

## Demonstração

Para uma visão detalhada da análise e dos resultados de clusterização, acesse o relatório completo em PDF:

[Visualizar Relatório de Clusters (PDF)](/report/relatorio_clusters.pdf)

## Funcionalidades

* **Coleta e Pré-processamento de Dados:** Carregamento de dados brutos e aplicação de técnicas de limpeza e normalização (StandardScaler) para preparar as variáveis numéricas.
* **Determinação do `K` Ideal:** Emprego de diversas métricas e visualizações robustas para identificar o número ótimo de clusters, incluindo:
    * Método do Cotovelo (Elbow Method)
    * Coeficiente de Silhueta (Silhouette Score)
    * Gap Statistic (implementado para maior controle)
    * Calinski-Harabasz Score
    * Davies-Bouldin Score
    * Visualizações interativas com Yellowbrick para validar a escolha.
* **Clusterização com K-Means:** Aplicação do algoritmo K-Means utilizando o `K` ideal para a segmentação dos produtos.
* **Redução de Dimensionalidade (PCA):** Utilização do PCA para projetar os dados em 2 dimensões, facilitando a visualização e interpretação dos clusters.
* **Geração Automatizada de Relatórios:** Criação de um relatório executivo em formato PDF (utilizando ReportLab), consolidando as análises, métricas e visualizações dos clusters.

## Tecnologias Utilizadas

As seguintes tecnologias e bibliotecas Python foram empregadas no desenvolvimento deste projeto:

* **Python**: Linguagem de programação principal.
* **Pandas**: Manipulação e análise eficiente de dados.
* **NumPy**: Suporte para operações numéricas e arrays.
* **Matplotlib**: Geração de gráficos e visualizações estáticas.
* **Seaborn**: Criação de gráficos estatísticos atraentes e informativos.
* **Scikit-learn (sklearn)**: Ferramentas para pré-processamento, algoritmos de clusterização (KMeans) e cálculo de métricas de avaliação.
* **Yellowbrick**: Biblioteca para visualizações de diagnóstico específicas para modelos de Machine Learning (ElbowVisualizer, SilhouetteVisualizer).
* **ReportLab**: Geração programática de documentos PDF para relatórios executivos.
* **Jupyter Notebook**: Ambiente interativo para desenvolvimento, execução e documentação da análise.

## Estrutura do Projeto

Este repositório está organizado da seguinte forma:

* `dados/`: Contém os dados brutos utilizados no projeto.
* `img/`: Diretório onde os gráficos e visualizações gerados são salvos.
* `notebooks/`: Contém os notebooks Jupyter que documentam o processo de análise, desde o pré-processamento até a clusterização e geração do relatório.
* `report/`: Onde o relatório final em PDF (`relatorio_clusters.pdf`) é salvo.
* `src/`: Contém os arquivos `.py` com o código-fonte principal do projeto.
* `.gitignore`: Arquivo para ignorar arquivos e pastas específicos do controle de versão do Git.
* `LICENSE.md`: Arquivo contendo a licença do projeto (MIT).
* `README.md`: Este arquivo, com a documentação do projeto.
* `requirements.txt`: Lista de todas as dependências Python necessárias para o projeto.

## ⚙️ Como Executar o Projeto

Para replicar e executar este projeto em seu ambiente, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/SeuUsuario/Projeto_Clusterizacao_777.git](https://github.com/SeuUsuario/Projeto_Clusterizacao_777.git)
    cd Projeto_Clusterizacao_777
    ```

2.  **Crie um ambiente virtual (opcional, mas recomendado):**

    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute os notebooks:**
    Os notebooks na pasta `notebooks/` contêm o fluxo completo da análise, desde o pré-processamento até a clusterização e geração do relatório. Recomenda-se executá-los sequencialmente para reproduzir os resultados.

    ```bash
    jupyter notebook
    ```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias, novas funcionalidades ou correção de bugs.

## Licença:

Este projeto está licenciado sob a Licença MIT. Para mais detalhes, consulte o arquivo [LICENSE.md](LICENSE.md) na raiz do repositório.

## ✉️ Contato

Para dúvidas ou informações adicionais, entre em contato:

* **Nome:** Flávio Henrique Barbosa
* **LinkedIn:** [Flávio Henrique Barbosa | LinkedIn](https://www.linkedin.com/in/fl%C3%A1vio-henrique-barbosa-38465938)
* **Email:** flaviohenriquehb777@outlook.com

