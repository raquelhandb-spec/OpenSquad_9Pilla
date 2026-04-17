---
task: "Find and Rank Financial News"
order: 1
input: |
  - research_focus: Tema e período definidos pelo usuário (de squads/noticias-financeiras/output/research-focus.md)
output: |
  - news_list: Lista de 3-5 notícias ranqueadas com dados verificados e hipóteses de ângulo
---

# Find and Rank Financial News

Pesquisa as principais notícias do mercado financeiro brasileiro no período e tema definidos pelo usuário, verifica os dados em fontes primárias e entrega uma lista ranqueada com hipótese de ângulo para cada notícia.

## Process

1. **Lê o arquivo de foco da pesquisa** (`output/research-focus.md`) para entender o tema específico e o período solicitado pelo usuário.

2. **Executa buscas web** com as seguintes queries (adapta ao tema recebido):
   - `"[tema] mercado financeiro Brasil [período]" site:valoreconomico.com.br OR site:infomoney.com.br OR site:bloomberg.com.br`
   - `"IPCA Selic câmbio dólar B3 Ibovespa [período]"` — se o tema for geral
   - `"[empresa/setor específico] resultado impacto [período]"` — se o tema for específico
   - Busca adicional nas fontes primárias: BACEN, IBGE, CVM, B3, press releases

3. **Verifica cada dado-chave** em pelo menos 2 fontes independentes. Se houver conflito entre fontes, registra ambas as versões.

4. **Ranqueia as notícias** pelo seguinte critério (ordem de prioridade):
   1. Impacto direto no bolso do brasileiro comum (inflação, juros, câmbio, emprego)
   2. Frescor (mais recente = mais pontos)
   3. Potencial de engajamento (dado surpreendente, comparação histórica, polêmica)
   4. Relevância para investidores (Ibovespa, renda fixa, fundos)

5. **Formata o output** com a estrutura abaixo para cada notícia.

## Output Format

```markdown
# Notícias Financeiras — [Data da pesquisa]
Tema pesquisado: [tema do research-focus.md]
Período: [período do research-focus.md]
Fontes consultadas: [lista de portais e fontes primárias]

---

## 🥇 Notícia 1 (Melhor para carrossel)

**Título:** [título jornalístico claro]
**Fonte:** [portal] — [URL completa]
**Data:** [YYYY-MM-DD]
**Fonte primária:** [BACEN/IBGE/empresa/etc] — [URL se disponível]

**Dado-chave:** [o número ou fato central — ex: "IPCA-15 de março veio em +0,44%, acima da expectativa de +0,38%"]
**Confiança:** Alta / Média / Baixa — [justificativa em 1 linha]

**Por que importa para o seguidor 9Pilla:**
[1-2 frases conectando a notícia ao cotidiano do seguidor — ex: "Significa que a inflação ainda pressiona o custo de vida, especialmente alimentos e serviços"]

**Hipótese de ângulo:**
[1 frase sugerindo como abordar — ex: "Ângulo educativo: explicar o que é IPCA-15 e por que veio acima do esperado prejudica quem tem renda fixa"]

---

## 🥈 Notícia 2

[mesmo formato]

---

## 🥉 Notícia 3

[mesmo formato]

---

## Notícia 4 (opcional)

[mesmo formato]

---

## Notícia 5 (opcional)

[mesmo formato]
```

## Output Example

> Referência de qualidade — não usar como template fixo.

```markdown
# Notícias Financeiras — 2026-04-07
Tema pesquisado: mercado financeiro geral
Período: Últimas 24 horas
Fontes consultadas: Valor Econômico, InfoMoney, BACEN, IBGE, Bloomberg Brasil

---

## 🥇 Notícia 1 (Melhor para carrossel)

**Título:** IPCA-15 de março sobe 0,44%, acima das expectativas e pressiona o BC
**Fonte:** Valor Econômico — https://valor.globo.com/financas/noticia/2026/03/25/ipca-15.ghtml
**Data:** 2026-03-25
**Fonte primária:** IBGE — https://ibge.gov.br/estatisticas/economicas/precos-custos-e-indices-de-precos/9348-ipca-15.html

**Dado-chave:** +0,44% em março de 2026, contra expectativa de +0,38% do mercado; acumulado 12 meses: +3,90%
**Confiança:** Alta — dado do IBGE confirmado por Valor, InfoMoney e Bloomberg Brasil

**Por que importa para o seguidor 9Pilla:**
Inflação acima do esperado significa que a poupança perde poder de compra mais rápido do que os rendimentos compensam. Passagem aérea subiu 5,94% só em março, alimentação no domicílio +0,55%.

**Hipótese de ângulo:**
Ângulo de problema invisível: "Você sabia que seu dinheiro está perdendo valor mesmo sem você gastar mais?" — explica IPCA, conecta à Selic e apresenta alternativas à poupança.

---

## 🥈 Notícia 2

**Título:** Saudi Aramco eleva preço do petróleo para a Ásia em quase US$20 — maior alta desde 2022
**Fonte:** InfoMoney — https://infomoney.com.br/economia/saudi-aramco-preco-petroleo/
**Data:** 2026-04-06
**Fonte primária:** Saudi Aramco Official Statement

**Dado-chave:** Prêmio elevado em ~US$20/barril, mais que o dobro do recorde anterior de 2022
**Confiança:** Média — confirmado por Bloomberg e InfoMoney; declaração oficial da Aramco em inglês, sem tradução verificada

**Por que importa para o seguidor 9Pilla:**
Impacto positivo para a Petrobras e para o saldo da balança comercial brasileira. Pode reduzir pressão fiscal e beneficiar fundos com exposição a commodities.

**Hipótese de ângulo:**
Ângulo de revelação positiva surpreendente: "Crise no petróleo mundial pode beneficiar o Brasil — entenda por quê."
```

## Quality Criteria

- [ ] Mínimo 3 notícias entregues (máximo 5)
- [ ] Cada notícia tem todos os campos preenchidos (título, fonte, data, dado-chave, confiança, relevância, ângulo)
- [ ] Pelo menos 1 notícia com confiança "Alta" (fonte primária verificada)
- [ ] Todas as notícias pertencem ao período solicitado pelo usuário
- [ ] Nenhuma notícia sem hipótese de ângulo

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Menos de 3 notícias entregues sem explicação das lacunas
2. Qualquer notícia com dado-chave sem fonte verificável (URL acessível)
