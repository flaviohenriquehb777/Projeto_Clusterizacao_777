# Projeto de Clusterização de Produtos da Amazon

Este projeto tem como objetivo principal aplicar técnicas de **machine learning não supervisionado** para identificar grupos (clusters) de produtos semelhantes com base em suas características. A clusterização auxilia na **segmentação de produtos**, possibilitando uma análise mais estratégica em campanhas de marketing, organização de catálogos e personalização de recomendações.

## Etapas do Projeto

1. **Carregamento dos Dados**  
   Os dados dos produtos da Amazon são carregados e preparados para análise.

2. **Pré-processamento**  
   Inclui normalização das variáveis com `StandardScaler`, remoção de colunas irrelevantes e seleção de atributos numéricos adequados para os algoritmos de clusterização.

3. **Determinação do número ideal de clusters (K)**  
   Diversas abordagens são utilizadas para encontrar o melhor valor de `k`:
   - **Método do Cotovelo (Elbow Method)**
   - **Índice de Silhueta (Silhouette Score)**
   - **Gap Statistic** (implementado manualmente)
   - **Calinski-Harabasz Score**
   - **Davies-Bouldin Score**
   - **Visualizações com Yellowbrick**

4. **Aplicação do KMeans**  
   Com o valor ideal de `k` determinado, o algoritmo KMeans é utilizado para realizar a clusterização.

5. **Redução de Dimensionalidade com PCA**  
   Aplicado para visualizar os clusters em 2D de forma mais interpretável.

6. **Geração de Relatório em PDF**  
   Um relatório automático em PDF é gerado utilizando a biblioteca `ReportLab`, contendo visualizações e estatísticas do modelo treinado.

## Tecnologias e Bibliotecas Utilizadas

- **Pandas / NumPy** – Manipulação e análise de dados
- **Matplotlib / Seaborn** – Visualizações gráficas
- **Scikit-learn** – Pré-processamento, algoritmos de clusterização e métricas
- **Yellowbrick** – Visualizações específicas para clustering (Elbow e Silhouette)
- **PCA** – Redução de dimensionalidade
- **ReportLab** – Geração automatizada de relatórios em PDF
- **Python** – Linguagem principal do projeto

## Resultados Esperados

- Segmentação clara dos produtos da Amazon em grupos distintos.
- Geração de insights visuais e estatísticos para stakeholders.
- Automatização do processo de relatório para fins de apresentação.

---

> 🔍 Este projeto pode ser facilmente adaptado para segmentação de clientes, análise de comportamento de usuários ou categorização de conteúdos em outros contextos de negócio.

