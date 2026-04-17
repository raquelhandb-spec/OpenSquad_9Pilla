---
execution: inline
agent: squads/noticias-financeiras/agents/carlos-carrossel
inputFile: squads/noticias-financeiras/output/news-list.md
outputFile: squads/noticias-financeiras/output/angles.md
---

# Step 04: Geração de Ângulos

## Context Loading

Carregue estes arquivos antes de executar:
- `squads/noticias-financeiras/output/news-list.md` — todas as notícias pesquisadas (para entender o contexto da notícia selecionada)
- `squads/noticias-financeiras/pipeline/data/tone-of-voice.md` — os 6 tons disponíveis da 9Pilla
- `squads/noticias-financeiras/pipeline/data/domain-framework.md` — frameworks de ângulo do mercado financeiro
- `squads/noticias-financeiras/pipeline/data/output-examples.md` — exemplos de ângulos bem-sucedidos

## Instructions

### Process
1. Identifique a notícia escolhida pelo usuário no checkpoint anterior (step-03).
2. Extraia o fato central, o dado-chave e o impacto no Brasil da notícia selecionada.
3. Leia o `tone-of-voice.md` para conhecer os tons disponíveis.
4. Gere 5 ângulos genuinamente distintos usando os 5 frameworks emocionais: Medo/Urgência, Oportunidade/Janela, Educativo/Revelação, Contrário/Mito, Inspiracional/Transformação.
5. Para cada ângulo: nome, tom sugerido, hook completo (primeira linha do slide 1), promessa implícita, perfil do fechamento.
6. Apresente os 5 ângulos numerados e peça ao usuário para escolher.

## Output Format

```markdown
# 5 Ângulos para: [Título da Notícia]
Notícia: [resumo em 1 linha]
Dado-chave: [número ou fato central]

---

## Ângulo 1 — [Nome]
**Tom:** [tom do tone-of-voice.md]
**Hook:** "[primeira linha do slide 1]"
**Promessa:** [o que o leitor vai aprender/ganhar]
**Fechamento:** [como o carrossel terminaria]

[repetir para ângulos 2-5]

---
Qual ângulo você quer desenvolver?
```

## Output Example

```markdown
# 5 Ângulos para: IPCA-15 sobe 0,44% em março, acima das expectativas
Notícia: Inflação medida pelo IPCA-15 veio acima do esperado em março de 2026, acumulando 3,90% em 12 meses.
Dado-chave: +0,44% março 2026; poupança rende 6,17% a.a.; passagem aérea +5,94%

---

## Ângulo 1 — Problema Invisível
**Tom:** Educativo-Próximo
**Hook:** "Você sabia que o seu dinheiro está perdendo valor todos os meses — mesmo sem você gastar mais?"
**Promessa:** O leitor vai entender inflação real e descobrir que a poupança não protege
**Fechamento:** 3 investimentos simples + CTA turma 9Pilla

## Ângulo 2 — Urgência
**Tom:** Urgente-Direto
**Hook:** "A inflação de março veio ACIMA do esperado. Isso muda tudo para quem está na poupança."
**Promessa:** Por que este momento é crítico para sair da poupança
**Fechamento:** Comparativo poupança vs CDB vs Tesouro + CTA

## Ângulo 3 — Mito Desconstruído
**Tom:** Analítico-Desafiador
**Hook:** "A poupança é isenta de IR. Isso não quer dizer que ela é um bom investimento."
**Promessa:** Desmonta o mito de que isenção de IR = melhor retorno
**Fechamento:** Cálculo real + contraste binário →

## Ângulo 4 — Contexto Global
**Tom:** Analítico-Informativo
**Hook:** "A guerra no Oriente Médio chegou na sua cozinha. Veja o caminho."
**Promessa:** Mecanismo completo: conflito → petróleo → frete → alimentos → IPCA
**Fechamento:** Como entender as causas muda a forma de se proteger

## Ângulo 5 — Transformação
**Tom:** Motivacional-Próximo
**Hook:** "Há 5 anos eu não entendia IPCA. Hoje sei como me proteger."
**Promessa:** Jornada de transformação + identificação com a audiência
**Fechamento:** Manifesto 9Pilla + CTA turma

---
Qual ângulo você quer desenvolver?
```

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Menos de 5 ângulos entregues
2. Dois ou mais ângulos com o mesmo tom E estrutura emocional

## Quality Criteria

- [ ] Exatamente 5 ângulos com estrutura emocional genuinamente distinta
- [ ] Hook completo (primeira linha escrita, não apenas descrita) para cada ângulo
- [ ] Output encerra com pergunta de escolha para o usuário
