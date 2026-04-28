# Amazon Product Intelligence — Business Questions Report

## Executive KPIs

- Total products: 1.351
- Average rating: 4.09
- Average discount: 46.69%
- Top category: Electronics
- Best PSI: Amazon Basics High-Speed HDMI Cable, 6 Feet (2-Pack),Black (PSI 87.74)

## Questions & Answers

### 1. Qual é o volume e a distribuição de produtos por categoria principal e subcategoria?

**Answer:** Total de produtos: 1.351. Top categoria: Electronics (490).

**Insight:** A concentração em poucas categorias sugere oportunidades claras de segmentação e otimização por vertical.

**Recommendation:** Priorizar ações nas maiores categorias e replicar a abordagem nas menores com maior crescimento.

### 2. Qual é a taxa de completude dos dados? Existem produtos sem avaliação ou com dados críticos ausentes?

**Answer:** Missing médio em campos críticos: 0.03%. Produtos sem rating: 0.07%. Produtos sem rating_count: 0.15%.

**Insight:** Campos de preço e rating são a base para PSI e clusterização; faltas reduzem comparabilidade.

**Recommendation:** Tratar nulos com imputação no pipeline e isolar itens com dados insuficientes para evitar distorções.

### 3. Qual é a distribuição de preços por categoria? Existem outliers extremos que distorcem a análise?

**Answer:** Outliers (IQR) em preço descontado: 15.47% dos produtos.

**Insight:** Outliers tendem a inflar médias; mediana e quartis são mais robustos para comparação por categoria.

**Recommendation:** Usar mediana/IQR em comparações e aplicar filtros ao analisar extremos.

### 4. Quais categorias oferecem os maiores descontos médios? Os descontos estão correlacionados com ratings mais altos ou mais baixos?

**Answer:** Maior desconto médio: HomeImprovement (57.50%). Correlação Spearman desconto×rating: -0.150.

**Insight:** Desconto alto não implica necessariamente melhor percepção; a correlação orienta estratégias por categoria.

**Recommendation:** Ajustar campanhas por categoria considerando o efeito observado em rating.

### 5. Existe uma faixa de preço ideal onde os produtos concentram as melhores avaliações?

**Answer:** Maior rating médio por faixa_preco: luxury (rating médio 4.19).

**Insight:** O melhor rating médio por faixa pode indicar um sweet spot de valor percebido.

**Recommendation:** Otimizar sortimento e promoções para maximizar presença na faixa com melhor rating médio.

### 6. Qual é o desconto médio praticado por categoria e qual categoria entrega mais valor real ao consumidor (desconto + rating alto)?

**Answer:** Categoria com maior score (desconto×rating): HomeImprovement (244.50).

**Insight:** Combinar desconto e rating evita promover itens baratos mas mal avaliados.

**Recommendation:** Usar o score de valor para priorizar vitrines e campanhas.

### 7. Produtos com desconto acima de 50% têm performance de avaliação diferente dos demais?

**Answer:** Diferença de rating médio (desconto>50% − <=50%): -0.073.

**Insight:** Diferença pequena sugere que desconto não é o único driver de satisfação.

**Recommendation:** Cruzar com volume de reviews e métricas operacionais (quando disponíveis) para validar promoções agressivas.

### 8. Quais são os produtos mais bem avaliados com alto volume de reviews (os verdadeiros líderes)?

**Answer:** Top líder: Swiffer Instant Electric Water Heater Faucet Tap Home-Kitchen Instantaneous Water Heater Tank less for Tap, LED Electric Head Water Heaters Tail Gallon Comfort(3000W) ((Pack of 1)) (rating 4.80, reviews 53.803).

**Insight:** Líderes combinam reputação e escala, sendo âncoras de confiança para a categoria.

**Recommendation:** Proteger disponibilidade e ranqueamento desses itens e usar como benchmark.

### 9. Existe correlação entre o número de avaliações e o rating médio?

**Answer:** Correlação Spearman rating_count×rating: 0.193.

**Insight:** Popularidade não garante satisfação; a relação ajuda a guiar estratégia por categoria.

**Recommendation:** Separar líderes, hidden gems e problemas populares para ações distintas.

### 10. Quais produtos têm alto rating mas pouquíssimas avaliações (potenciais hidden gems)?

**Answer:** Exemplo: Syncwire LTG to USB Cable for Fast Charging Compatible with Phone 5/ 5C/ 5S/ 6/ 6S/ 7/8/ X/XR/XS Max/ 11/12/ 13 Series and Pad Air/Mini, Pod & Other Devices (1.1 Meter, White) (rating 5.00, reviews 5).

**Insight:** Hidden gems tendem a ter boa qualidade mas baixa descoberta.

**Recommendation:** Testar boosts de visibilidade para validar potencial de escala.

### 11. Quais produtos têm muitas avaliações mas rating baixo (produtos problemáticos populares)?

**Answer:** Exemplo: boAt Airdopes 121v2 in-Ear True Wireless Earbuds with Upto 14 Hours Playback, 8MM Drivers, Battery Indicators, Lightweight Earbuds & Multifunction Controls (Active Black, with Mic) (rating 3.80, reviews 180.998).

**Insight:** Itens com alto volume e baixa nota são riscos reputacionais.

**Recommendation:** Auditar causas em reviews e priorizar correções.

### 12. Qual é o ranking de produtos usando o Product Score Index combinando rating, volume de reviews e desconto?

**Answer:** #1 por PSI: Amazon Basics High-Speed HDMI Cable, 6 Feet (2-Pack),Black (PSI 87.74).

**Insight:** PSI reduz viés de avaliar apenas por rating ou apenas por desconto.

**Recommendation:** Usar PSI como critério de curadoria e comparação entre subcategorias.

### 13. Quais são os Top 10 produtos por PSI em cada categoria principal?

**Answer:** Top 10 por categoria exportado em reports/psi_top10_by_category.csv (linhas: 47).

**Insight:** Ranking por categoria evita comparar produtos incomparáveis.

**Recommendation:** Usar Top 10 por categoria como shortlist para campanhas.

### 14. Como os clusters de produtos se distribuem no espaço PSI vs. preço?

**Answer:** Distribuição no dashboard: PSI vs preço colorido por cluster (clusters: 5).

**Insight:** A relação PSI×preço por cluster mostra onde existe alto valor percebido em diferentes faixas.

**Recommendation:** Atuar por cluster com estratégias específicas de preço e promo.

### 15. Quantos clusters de produtos existem naturalmente na base (usar Elbow + Silhouette)?

**Answer:** Clusters usados no modelo final: 5 (ver notebook 04 para Elbow + Silhouette).

**Insight:** O número de clusters sintetiza padrões de mercado em grupos acionáveis.

**Recommendation:** Reavaliar k periodicamente ao expandir a base.

### 16. Quais são os perfis de cada cluster? (ex: premium bem avaliado, barato com alto desconto, popular problemático)

**Answer:** Perfis e métricas médias por cluster disponíveis no dashboard (cards e tabela).

**Insight:** Clusters transformam variáveis contínuas em segmentos com narrativa e estratégia.

**Recommendation:** Atribuir uma estratégia por cluster (pricing, promo, sortimento) e medir impacto.

### 17. Qual cluster representa a maior oportunidade de negócio para a Amazon?

**Answer:** Cluster com maior score (rating×desconto): 4 — barato com alto desconto (score 259.28).

**Insight:** A oportunidade combina qualidade percebida e atratividade de preço.

**Recommendation:** Focar visibilidade/estoque nesse cluster e validar uplift em conversão.

### 18. Qual é o sentimento predominante nos títulos e conteúdos dos reviews por categoria?

**Answer:** Exemplo: em Car&Motorbike, sentimento predominante é positivo (share 100.00%).

**Insight:** Sentimento por categoria complementa rating e pode antecipar problemas de experiência.

**Recommendation:** Monitorar categorias com maior share negativo e cruzar com produtos populares.

### 19. Existe divergência entre o sentimento textual do review e o rating numérico dado?

**Answer:** Share de reviews com rating>=4 e sentimento negativo: 1.37%.

**Insight:** Divergência sugere que o texto traz nuances além do rating.

**Recommendation:** Usar sentimento como sinal adicional para triagem de problemas.

### 20. Quais palavras mais frequentes aparecem em reviews positivos vs. negativos?

**Answer:** Top positivos: [('quality', 3099), ('use', 2015), ('price', 1841), ('nice', 1826), ('can', 1745), ('one', 1708), ('cable', 1677), ('like', 1300), ('from', 1268), ('best', 1255), ('phone', 1254), ('money', 1237)]. Top negativos: [('quality', 82), ('working', 53), ('one', 48), ('service', 47), ('from', 45), ('money', 41), ('after', 40), ('use', 40), ('will', 38), ('installation', 37), ('cable', 35), ('nice', 34)].

**Insight:** As palavras destacam drivers de satisfação e dor.

**Recommendation:** Usar essas palavras como vocabulário de monitoramento.
