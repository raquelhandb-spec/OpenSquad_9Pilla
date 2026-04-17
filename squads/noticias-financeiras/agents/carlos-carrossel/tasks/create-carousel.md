---
task: "Create Carousel"
order: 2
input: |
  - selected_angle: Ângulo escolhido pelo usuário (do angles.md, via checkpoint)
  - selected_news: Notícia com dados verificados (do news-list.md)
  - tone_of_voice: Tom específico do ângulo escolhido
  - instagram_feed_format: Regras da plataforma (injetado pelo Pipeline Runner)
output: |
  - carousel_draft: Copy completo do carrossel — todos os slides + legenda + CTA
---

# Create Carousel

Escreve o copy completo do carrossel de Instagram para a 9Pilla, baseado no ângulo aprovado pelo usuário. Entrega todos os slides com headline + texto de suporte, a legenda completa com estrutura de índice (→), e o CTA final.

## Process

1. **Confirma o ângulo escolhido** e o tom correspondente do `tone-of-voice.md`. Lê o ângulo com o hook aprovado.

2. **Lê a notícia selecionada** do `news-list.md` para usar os dados verificados nos slides.

3. **Lê o `domain-framework.md`** para seguir a estrutura de 6 slides recomendada pela investigação.

4. **Escreve os slides** seguindo a estrutura padrão de carrossel financeiro da 9Pilla:
   - **Slide 1 — Hook**: Usa exatamente o hook do ângulo aprovado. Headline bold + subtext de contexto. Máximo 15 palavras no headline.
   - **Slides 2-4 — Desenvolvimento**: Um conceito ou dado por slide. Headline de insight (10-15 palavras) + 2-3 linhas de suporte (dado + contexto + âncora cotidiana). Mínimo 40 palavras por slide.
   - **Slide 5 — Contraste/Solução**: Estrutura binária (→ quem X / → quem Y) ou lista de 3 ações práticas.
   - **Slide 6 — CTA + Manifesto**: Pergunta de engajamento + frase de manifesto da 9Pilla + CTA de produto/follow.

5. **Escreve a legenda** com:
   - Hook (primeiros 125 caracteres — visíveis antes do "ver mais")
   - Índice com → listando os slides
   - CTA de produto ou engajamento
   - Frase de manifesto
   - (Opcional) 5-10 hashtags temáticos no final

6. **Revisa o copy completo** checando: dado verificado presente, tom consistente, contraste no slide 5, CTA no slide 6, legenda com índice.

## Output Format

```markdown
# Carrossel Draft — [Título da Notícia] — Ângulo: [Nome do Ângulo]
Tom: [tom escolhido]
Data: [YYYY-MM-DD]

---

## SLIDES

### Slide 1 — Hook
**Headline:** [máx 15 palavras, bold]
**Subtext:** [contexto em 1-2 linhas]

### Slide 2 — [Subtítulo do conceito]
**Headline:** [insight em 10-15 palavras]
**Suporte:** [dado + contexto + âncora cotidiana — mín 40 palavras total no slide]

### Slide 3 — [Subtítulo]
**Headline:** [...]
**Suporte:** [...]

### Slide 4 — [Subtítulo]
**Headline:** [...]
**Suporte:** [...]

### Slide 5 — Contraste / Solução
**Headline:** [...]
→ [quem entende / faz X]: [resultado positivo]
→ [quem não entende / não faz X]: [resultado negativo]
**Ou:** 3 ações práticas numeradas

### Slide 6 — CTA + Manifesto
**Pergunta de engajamento:** [pergunta que convida comentário]
**Manifesto:** [frase de posicionamento da 9Pilla]
**CTA:** [ação específica — lista de espera, follow, salvar]

---

## LEGENDA

[Hook — primeiros 125 caracteres]

Neste carrossel:
→ [tópico do slide 2]
→ [tópico do slide 3]
→ [tópico do slide 4]
→ [tópico do slide 5]
→ [CTA/tópico do slide 6]

[CTA de produto ou engajamento]

[Frase de manifesto]

[hashtags opcionais]
```

## Output Example

> Referência de qualidade — carrossel completo baseado na investigação.

```markdown
# Carrossel Draft — IPCA-15 Março 2026 — Ângulo: Problema Invisível
Tom: Educativo-Próximo
Data: 2026-04-07

---

## SLIDES

### Slide 1 — Hook
**Headline:** Seu dinheiro está perdendo valor — mesmo sem você gastar mais
**Subtext:** A inflação acumulou +3,90% em 12 meses. Veja o que isso significa para você.

### Slide 2 — O que é inflação, de verdade
**Headline:** Inflação não é só preço subindo. É o seu dinheiro encolhendo.
**Suporte:** O IPCA-15 de março veio em +0,44%, acima do esperado (+0,38%). Em 12 meses, acumulamos +3,90%. Isso significa que R$ 1.000 de hoje compram o que R$ 962 compravam há um ano. A sua feira ficou mais cara, o restaurante aumentou sem avisar, a passagem aérea subiu 5,94% só em março.

### Slide 3 — Por que a guerra no Oriente Médio chegou na sua cozinha
**Headline:** O caminho do conflito até o seu carrinho de supermercado
**Suporte:** Conflito no Oriente Médio → preço do barril de petróleo sobe → custo do frete internacional aumenta → produtos importados ficam mais caros → alimentos processados e industrializados sobem no Brasil. Não é coincidência — é o mercado global funcionando.

### Slide 4 — A poupança não te protege de verdade
**Headline:** A poupança rende 6,17% ao ano. A inflação consumiu 3,90%.
**Suporte:** Parece que sobrou 2,27%, certo? Mas esse rendimento é bruto. E a poupança não te dá acesso às melhores taxas do mercado. CDB de banco grande paga em torno de 100% do CDI — hoje perto de 10,5% ao ano. Mesmo após o IR, você sai bem à frente.

### Slide 5 — O que fazer agora
**Headline:** Dois caminhos. Você escolhe qual.
→ Quem entende a inflação: antecipa, protege a carteira com Tesouro IPCA+ e CDB e mantém poder de compra
→ Quem ignora: fica na poupança e perde para a inflação todo mês, sem perceber

Três movimentos simples:
1. Sai da poupança para um CDB de liquidez diária (começa com qualquer valor)
2. Reserva de emergência no Tesouro Selic (seguro e rentável)
3. Sobra mensal em Tesouro IPCA+ (proteção de longo prazo)

### Slide 6 — CTA + Manifesto
**Pergunta de engajamento:** Você ainda tem dinheiro na poupança? Comenta aqui — sem julgamento.
**Manifesto:** O problema nunca foi o dinheiro. Foi o acesso à informação.
**CTA:** 🚨 A 1ª turma 9Pilla está chegando. De gastadora a investidora em 9 semanas. Entre na lista de espera: link na bio.

---

## LEGENDA

Seu dinheiro está perdendo valor todos os meses — mesmo sem você gastar mais.

A inflação acumulou +3,90% em 12 meses. O IPCA-15 de março veio em +0,44%, acima do esperado. Isso significa que a sua feira ficou mais cara, o restaurante aumentou sem avisar, a passagem aérea subiu 5,94% só em março.

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

## Quality Criteria

- [ ] Exatamente 6 slides escritos (ou 7-8 se o conteúdo justificar, máximo 10)
- [ ] Slide 1 usa exatamente o hook aprovado pelo usuário
- [ ] Pelo menos 1 dado verificado incluído com número preciso
- [ ] Slide 5 tem estrutura binária → ou lista de 3 ações
- [ ] Slide 6 tem pergunta de engajamento + manifesto + CTA
- [ ] Legenda tem os primeiros 125 caracteres como hook + índice com →
- [ ] Tom consistente do ângulo escolhido em todos os slides

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Algum slide sem dado, exemplo ou metáfora de ancoragem (slides de texto puro genérico)
2. Legenda sem índice de slides com →
