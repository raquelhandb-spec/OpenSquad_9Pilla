---
execution: inline
agent: squads/noticias-financeiras/agents/carlos-carrossel
format: instagram-feed
inputFile: squads/noticias-financeiras/output/angles.md
outputFile: squads/noticias-financeiras/output/carousel-draft.md
---

# Step 06: Criação do Carrossel

## Context Loading

Carregue estes arquivos antes de executar:
- `squads/noticias-financeiras/output/angles.md` — ângulos gerados (para identificar o ângulo escolhido pelo usuário e o hook aprovado)
- `squads/noticias-financeiras/output/news-list.md` — notícia com dados verificados (para usar os números corretos)
- `squads/noticias-financeiras/pipeline/data/tone-of-voice.md` — escolhe o tom correspondente ao ângulo selecionado
- `squads/noticias-financeiras/pipeline/data/domain-framework.md` — estrutura de 6 slides recomendada
- `squads/noticias-financeiras/pipeline/data/output-examples.md` — referência de carrosséis de alta qualidade
- `_opensquad/core/best-practices/instagram-feed.md` — regras da plataforma (injetado pelo Pipeline Runner)

## Instructions

### Process
1. Identifique o ângulo escolhido pelo usuário e o hook aprovado.
2. Leia o tom correspondente no `tone-of-voice.md`.
3. Escreva o carrossel completo seguindo a estrutura de 6 slides do `domain-framework.md`: Hook → Contexto → Mecanismo → Impacto no bolso → Contraste/Solução → CTA + Manifesto.
4. Inclua pelo menos 1 dado verificado (com número preciso) da pesquisa da Nara.
5. Escreva a legenda com: hook nos primeiros 125 caracteres, índice com → listando os slides, CTA de produto/engajamento, frase de manifesto da 9Pilla.
6. Use o hook exatamente como aprovado no step-05 (não reescreve sem justificativa).

## Output Format

```markdown
# Carrossel Draft — [Título da Notícia] — Ângulo: [Nome]
Tom: [tom]
Data: [YYYY-MM-DD]

---

## SLIDES

### Slide 1 — Hook
**Headline:** [máx 15 palavras]
**Subtext:** [contexto em 1-2 linhas]

### Slide 2 — [Subtítulo]
**Headline:** [insight em 10-15 palavras]
**Suporte:** [dado + contexto + âncora cotidiana — mínimo 40 palavras total]

### Slide 3 — [Subtítulo]
[mesmo formato]

### Slide 4 — [Subtítulo]
[mesmo formato]

### Slide 5 — Contraste / Solução
**Headline:** [...]
→ [positivo]: [resultado]
→ [negativo]: [consequência]

### Slide 6 — CTA + Manifesto
**Pergunta:** [pergunta de engajamento]
**Manifesto:** [frase de posicionamento 9Pilla]
**CTA:** [ação específica]

---

## LEGENDA

[Hook — primeiros 125 caracteres]

[Contexto em 2-3 linhas]

Neste carrossel:
→ [slide 2]
→ [slide 3]
→ [slide 4]
→ [slide 5]
→ [slide 6/CTA]

[CTA de produto ou engajamento]

[Frase de manifesto]

[hashtags opcionais]
```

## Output Example

```markdown
# Carrossel Draft — IPCA-15 Março 2026 — Ângulo: Problema Invisível
Tom: Educativo-Próximo
Data: 2026-04-07

---

## SLIDES

### Slide 1 — Hook
**Headline:** Seu dinheiro está perdendo valor — mesmo sem você gastar mais
**Subtext:** IPCA-15 de março: +0,44% acima do esperado. Veja o que isso muda para você.

### Slide 2 — O que é inflação, de verdade
**Headline:** Inflação não é só preço subindo. É o seu dinheiro encolhendo.
**Suporte:** O IPCA-15 de março veio em +0,44%, acima da expectativa de +0,38%. Em 12 meses, acumulamos +3,90%. R$ 1.000 de hoje compram o que R$ 962 compravam há um ano. A sua feira ficou mais cara, o restaurante aumentou sem avisar, a passagem aérea subiu 5,94% só em março.

### Slide 3 — Por que a guerra chegou na sua cozinha
**Headline:** O caminho do conflito até o seu carrinho de supermercado
**Suporte:** Conflito no Oriente Médio eleva o preço do barril → frete internacional sobe → produtos importados ficam mais caros → alimentos processados sobem no Brasil. Não é coincidência — é o mercado global funcionando em tempo real.

### Slide 4 — A poupança não te protege
**Headline:** Poupança rende 6,17% ao ano. A inflação consumiu 3,90%.
**Suporte:** Parece que sobrou 2,27%, certo? Mas o rendimento é bruto. Investimentos como CDB e Tesouro IPCA+ entregam muito mais — e mesmo após o IR, você sai bem à frente da inflação.

### Slide 5 — Dois caminhos
**Headline:** Dois caminhos. Você escolhe.
→ Quem entende: antecipa, protege a carteira com Tesouro IPCA+ e CDB, mantém poder de compra
→ Quem ignora: fica na poupança e perde para a inflação todo mês, sem perceber

### Slide 6 — CTA + Manifesto
**Pergunta:** Você ainda tem dinheiro na poupança? Comenta aqui — sem julgamento.
**Manifesto:** O problema nunca foi o dinheiro. Foi o acesso à informação.
**CTA:** 🚨 A 1ª turma 9Pilla está chegando. De gastadora a investidora em 9 semanas. Entre na lista de espera: link na bio.

---

## LEGENDA

Seu dinheiro está perdendo valor todos os meses — mesmo sem você gastar mais.

A inflação acumulou +3,90% em 12 meses. O IPCA-15 de março veio em +0,44%, acima do esperado. Sua feira ficou mais cara, o restaurante aumentou sem avisar, a passagem aérea subiu 5,94% só em março.

Neste carrossel:
→ O que é inflação e como ela corrói o seu bolso
→ Por que a guerra no Oriente Médio chegou na sua cozinha
→ O que a Selic tem a ver com tudo isso
→ Por que a poupança não te protege de verdade
→ 3 investimentos simples que qualquer pessoa pode fazer hoje

🚨 A 1ª turma 9Pilla está chegando.
De gastadora a investidora em 9 semanas — com método, acompanhamento e sem enrolação.
👉 Entre na lista de espera: link na bio

O problema nunca foi o dinheiro. Foi o acesso à informação.

#inflacao #ipca #investimentos #mercadofinanceiro #educacaofinanceira #poupanca #tesouredireto #9pilla
```

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Algum slide sem dado, exemplo ou metáfora de ancoragem concreta
2. Legenda sem índice de slides com →

## Quality Criteria

- [ ] 6 slides completos (todos os campos preenchidos)
- [ ] Slide 1 usa exatamente o hook aprovado no step-05
- [ ] Pelo menos 1 dado verificado incluído com número preciso
- [ ] Slide 5 com estrutura binária → ou lista de ações
- [ ] Slide 6 com pergunta + manifesto + CTA
- [ ] Legenda com hook (125 chars) + índice → + manifesto
