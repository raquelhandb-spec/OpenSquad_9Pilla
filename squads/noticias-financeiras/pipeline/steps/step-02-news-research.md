---
execution: subagent
agent: squads/noticias-financeiras/agents/nara-noticias
inputFile: squads/noticias-financeiras/output/research-focus.md
outputFile: squads/noticias-financeiras/output/news-list.md
model_tier: powerful
---

# Step 02: Pesquisa de Notícias

## Context Loading

Carregue estes arquivos antes de executar:
- `squads/noticias-financeiras/output/research-focus.md` — tema e período definidos pelo usuário
- `squads/noticias-financeiras/pipeline/data/research-brief.md` — contexto do mercado financeiro brasileiro e fontes confiáveis
- `squads/noticias-financeiras/pipeline/data/domain-framework.md` — critérios de ranqueamento de notícias

## Instructions

### Process
1. Leia o `research-focus.md` para extrair o tema e o período solicitado pelo usuário.
2. Execute buscas web nas principais fontes de jornalismo financeiro brasileiro: Valor Econômico, InfoMoney, Bloomberg Brasil, CNN Brasil Negócios, B3, Banco Central, IBGE.
3. Para cada notícia candidata, verifique o dado-chave em pelo menos 2 fontes independentes.
4. Ranqueie 3 a 5 notícias pelo critério: impacto no cotidiano do brasileiro > frescor > potencial de engajamento > relevância para investidores.
5. Para cada notícia, escreva uma hipótese de ângulo (como a 9Pilla poderia abordar essa notícia).

## Output Format

```markdown
# Notícias Financeiras — [Data]
Tema pesquisado: [tema]
Período: [período]
Fontes consultadas: [lista]

---

## 🥇 Notícia 1 (Melhor para carrossel)
**Título:** [título]
**Fonte:** [portal] — [URL]
**Data:** [data]
**Fonte primária:** [fonte] — [URL]
**Dado-chave:** [número ou fato central]
**Confiança:** Alta / Média / Baixa — [justificativa]
**Por que importa para o seguidor 9Pilla:** [1-2 frases]
**Hipótese de ângulo:** [1 frase]

[repetir para notícias 2 a 5]
```

## Output Example

```markdown
# Notícias Financeiras — 2026-04-07
Tema pesquisado: mercado financeiro geral
Período: Últimas 24 horas
Fontes consultadas: Valor Econômico, InfoMoney, BACEN, IBGE

---

## 🥇 Notícia 1

**Título:** IPCA-15 de março sobe 0,44%, acima das expectativas de 0,38%
**Fonte:** Valor Econômico — https://valor.globo.com/...
**Data:** 2026-03-25
**Fonte primária:** IBGE — https://ibge.gov.br/...
**Dado-chave:** +0,44% em março; acumulado 12 meses: +3,90%; passagem aérea +5,94%
**Confiança:** Alta — IBGE confirmado por Valor, InfoMoney e Bloomberg
**Por que importa:** Inflação acima do esperado pressiona o custo de vida e questiona a eficácia da poupança como proteção
**Hipótese de ângulo:** Problema invisível — "Seu dinheiro está perdendo valor mesmo sem você gastar mais"

---

## 🥈 Notícia 2
...
```

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Menos de 3 notícias entregues sem justificativa das lacunas
2. Alguma notícia com dado-chave sem URL de fonte verificável

## Quality Criteria

- [ ] 3 a 5 notícias ranqueadas com todos os campos preenchidos
- [ ] Todas as notícias do período solicitado
- [ ] Pelo menos 1 notícia com confiança "Alta"
- [ ] Cada notícia tem hipótese de ângulo
