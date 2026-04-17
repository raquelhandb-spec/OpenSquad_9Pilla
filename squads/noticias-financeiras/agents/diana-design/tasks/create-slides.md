---
task: "Create Slides"
order: 1
input: |
  - carousel_draft: Copy completo do carrossel aprovado (carousel-draft.md)
output: |
  - slides_report: Link do Canva + descrição de cada slide + anotações de adaptação
---

# Create Slides

Cria os slides do carrossel no Canva a partir do copy aprovado, aplicando a identidade visual da 9Pilla.

## Process

1. **Lê o `carousel-draft.md`** para entender todos os slides a criar: headline, suporte, CTA e manifesto de cada um.

2. **Abre o Canva** via MCP e busca um template de carrossel Instagram com identidade visual que combine com o tom do carrossel (educativo = mais clean/branco; urgente = mais escuro/vermelho; analítico = azul escuro/cinza).

3. **Cria um slide por vez**, nesta ordem:
   - **Slide 1 (capa)**: Fundo de destaque (cor ou foto editorial). Headline com máxima hierarquia. Logo da 9Pilla + @9pilla.link visíveis. Data ou "Notícia de hoje".
   - **Slides 2-4 (desenvolvimento)**: Alterna fundo (claro → escuro → acento). Headline bold no topo. Suporte em fonte menor abaixo. Destaca 1-2 palavras do headline em cor de acento.
   - **Slide 5 (contraste/solução)**: Fundo neutro ou de acento. Setas → visualmente destacadas. Dois blocos de texto (→ positivo / → negativo) ou lista numerada.
   - **Slide 6 (CTA)**: Fundo escuro ou de marca. Pergunta de engajamento + manifesto em destaque. CTA com destaque visual (botão, seta ou cor).

4. **Verifica cada slide** para legibilidade mobile: headline ≥ 43px, body ≥ 34px, contraste suficiente para leitura em fundo escuro ou claro.

5. **Exporta o design** em PNG 1080x1440px (formato 3:4, padrão Instagram Feed).

6. **Gera o output** com o link do Canva + descrição de cada slide.

## Output Format

```markdown
# Slides Report — [Título da Notícia]
Data: [YYYY-MM-DD]
Link Canva: [URL do design no Canva]
Slides criados: [N]

---

## Slide 1 — Capa
**Fundo:** [cor/foto/gradiente]
**Headline:** "[texto exato]" — [tamanho]px, bold
**Subtext:** "[texto]" — [tamanho]px
**Logo:** [posição]
**Acento:** [cor e onde foi aplicado]
**Adaptação:** [se o copy foi adaptado para o layout — o que mudou e por quê]

## Slide 2 — [Título]
[mesmo formato]

...

## Slide N — CTA
[mesmo formato]

---

## Notas de Design
[Qualquer observação sobre decisões de layout, sugestões de ajuste de copy para revisão, ou limitações do template escolhido]
```

## Output Example

> Referência de qualidade.

```markdown
# Slides Report — IPCA-15 Março 2026
Data: 2026-04-07
Link Canva: https://www.canva.com/design/DAxxxxxx/view
Slides criados: 6

---

## Slide 1 — Capa
**Fundo:** Azul escuro (#0D1B2A) com gradiente sutil
**Headline:** "Seu dinheiro está perdendo valor — mesmo sem gastar mais" — 52px, bold, branco
**Subtext:** "IPCA-15 de março: +0,44%" — 30px, medium, amarelo-acento
**Logo:** 9Pilla no canto inferior direito, branco
**Acento:** "perdendo valor" em amarelo #FFD700
**Adaptação:** Headline encurtado de "mesmo sem você gastar mais" para "mesmo sem gastar mais" (economizou 1 linha no layout)

## Slide 2 — O que é inflação, de verdade
**Fundo:** Branco (#FFFFFF)
**Headline:** "Inflação não é só preço subindo. É o seu dinheiro encolhendo." — 43px, bold, preto
**Suporte:** Dado completo com IPCA-15 — 32px, medium, cinza escuro
**Acento:** "encolhendo" em laranja #FF5A00
**Adaptação:** Nenhuma

## Slide 3 — Mecanismo global
**Fundo:** Cinza escuro (#1C1C1E)
**Headline:** "O caminho do conflito até o seu carrinho" — 46px, bold, branco
**Suporte:** Cadeia Oriente Médio → frete → alimentos — 32px, medium, cinza claro
**Acento:** "carrinho" em laranja
**Adaptação:** Nenhuma

## Slide 4 — Poupança vs realidade
**Fundo:** Branco
**Headline:** "Poupança rende 6,17% a.a. Inflação: 3,90%. Não parece ruim — mas é." — 40px
**Suporte:** Comparativo CDB — 32px
**Acento:** "mas é" em vermelho
**Adaptação:** Nenhuma

## Slide 5 — Contraste
**Fundo:** Azul escuro
**Headline:** "Dois caminhos:" — 48px, branco
**Setas:** "→ Quem entende" em verde / "→ Quem ignora" em vermelho — 36px each
**Adaptação:** Nenhuma

## Slide 6 — CTA
**Fundo:** Gradiente 9Pilla (azul escuro → roxo)
**Pergunta:** "Você ainda tem dinheiro na poupança?" — 40px, branco
**Manifesto:** "O problema nunca foi o dinheiro. Foi o acesso à informação." — 34px, itálico
**CTA:** "🚨 1ª turma 9Pilla — lista de espera: link na bio" — 32px, bold, amarelo
**Adaptação:** Nenhuma

---

## Notas de Design
Template escolhido: "Carrossel Educativo Dark Blue" da biblioteca Canva. Paleta aplicada: azul escuro (#0D1B2A), branco, laranja (#FF5A00) como acento principal. Todos os slides passaram no teste de legibilidade mobile (fonte mínima usada: 30px no subtext do slide 1).
```

## Quality Criteria

- [ ] Todos os slides do carousel-draft.md criados no Canva (nenhum omitido)
- [ ] Link do Canva incluído no output
- [ ] Slide 1 com logo e @handle da 9Pilla
- [ ] Alternância de fundo entre slides (nenhum fundo repetido em sequência)
- [ ] Headline mínimo 43px em todos os slides
- [ ] Body mínimo 34px em todos os slides
- [ ] Anotações de adaptação presentes quando o copy foi alterado

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Link do Canva ausente no output (sem link = sem design verificável)
2. Algum slide omitido em relação ao carousel-draft.md
