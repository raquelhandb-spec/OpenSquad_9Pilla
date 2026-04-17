---
execution: subagent
agent: squads/noticias-financeiras/agents/diana-design
inputFile: squads/noticias-financeiras/output/carousel-draft.md
outputFile: squads/noticias-financeiras/output/slides-report.md
model_tier: powerful
---

# Step 08: Criação dos Slides no Canva

## Context Loading

Carregue estes arquivos antes de executar:
- `squads/noticias-financeiras/output/carousel-draft.md` — copy completo aprovado (todos os slides + legenda)
- `squads/noticias-financeiras/pipeline/data/research-brief.md` — identidade visual e contexto da 9Pilla

## Instructions

### Process
1. Leia o `carousel-draft.md` para entender todos os slides a criar (headline + suporte de cada slide).
2. Acesse o Canva via MCP e busque um template de carrossel para Instagram compatível com o tom do carrossel (educativo = clean/branco, urgente = escuro/vermelho, analítico = azul escuro).
3. Crie o slide 1 (capa) com logo da 9Pilla + @9pilla.link + headline principal.
4. Crie os slides 2 a N alternando fundos (escuro → claro → acento, nunca dois iguais consecutivos).
5. Destaque 1-2 palavras-chave do headline de cada slide em cor de acento.
6. Crie o slide final (CTA) com gradiente da marca, pergunta de engajamento e manifesto em destaque.
7. Verifique legibilidade: headline ≥ 43px, body ≥ 34px. Sem números de slide no design.
8. Exporte o design como PNG/JPEG 1080x1440px.

## Output Format

```markdown
# Slides Report — [Título]
Data: [YYYY-MM-DD]
Link Canva: [URL]
Slides criados: [N]

---

## Slide 1 — Capa
**Fundo:** [...]
**Headline:** "[texto]" — [N]px, bold
**Logo:** [posição]
**Acento:** [cor e onde aplicado]
**Adaptação:** [se o copy foi adaptado]

[repetir para cada slide]

---

## Notas de Design
[decisões de layout, limitações do template, sugestões]
```

## Output Example

```markdown
# Slides Report — IPCA-15 Março 2026
Data: 2026-04-07
Link Canva: https://www.canva.com/design/DAxxxxxx/view
Slides criados: 6

---

## Slide 1 — Capa
**Fundo:** Azul escuro (#0D1B2A) com gradiente
**Headline:** "Seu dinheiro está perdendo valor — mesmo sem gastar mais" — 52px, bold, branco
**Logo:** 9Pilla inferior direito, branco; @9pilla.link inferior esquerdo, 28px
**Acento:** "perdendo valor" em amarelo #FFD700
**Adaptação:** Encurtado de "mesmo sem você gastar mais" para "mesmo sem gastar mais"

## Slide 2 — O que é inflação
**Fundo:** Branco (#FFFFFF)
**Headline:** "Inflação não é só preço subindo. É o seu dinheiro encolhendo." — 43px, bold, preto
**Acento:** "encolhendo" em laranja #FF5A00
**Adaptação:** Nenhuma

[...]
```

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Link Canva ausente no output
2. Algum slide do carousel-draft.md omitido no design

## Quality Criteria

- [ ] Link Canva incluído
- [ ] Todos os slides criados
- [ ] Slide 1 com logo e @handle da 9Pilla
- [ ] Alternância de fundos (sem repetição consecutiva)
- [ ] Headline ≥ 43px, body ≥ 34px em todos os slides
- [ ] Anotações de adaptação de copy documentadas
