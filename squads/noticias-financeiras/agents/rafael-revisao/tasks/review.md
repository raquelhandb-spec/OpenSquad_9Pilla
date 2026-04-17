---
task: "Review"
order: 1
input: |
  - slides_report: Design dos slides no Canva (slides-report.md)
  - carousel_draft: Copy completo do carrossel (carousel-draft.md)
  - news_list: Notícias com dados verificados (news-list.md) — para checar precisão dos dados
output: |
  - review_report: Veredito APROVADO/REPROVADO + feedback estruturado
---

# Review

Avalia o carrossel completo (copy + design) contra os critérios de qualidade da 9Pilla e dos top performers investigados. Emite veredito binário com feedback acionável.

## Process

1. **Lê os três inputs**: `slides-report.md` (design), `carousel-draft.md` (copy) e `news-list.md` (dados originais).

2. **Avalia o copy** em 4 dimensões:
   - **Hook**: Usa uma das 5 estruturas eficazes da investigação? Para o scroll? É específico para a notícia (não genérico)?
   - **Dados**: O dado-chave no copy bate com o dado da pesquisa da Nara? Está com número correto e âncora temporal?
   - **Estrutura**: Tem 6 slides com a sequência: Hook → Contexto → Mecanismo → Impacto → Contraste/Solução → CTA?
   - **Voz 9Pilla**: Tom consistente, manifesto presente, legenda com índice →, CTA claro?

3. **Avalia o design** em 3 dimensões:
   - **Legibilidade**: Headline ≥ 43px? Body ≥ 34px? Contraste adequado?
   - **Hierarquia visual**: Headline domina, suporte secundário, nenhum elemento competindo pelo olho?
   - **Identidade**: Logo no slide 1, alternância de fundos, acento de cor nos destaques?

4. **Classifica cada achado** como:
   - 🚫 **Bloqueador** — impede a publicação, precisa ser corrigido
   - ⚠️ **Sugestão** — melhoraria o resultado mas não bloqueia

5. **Emite o veredito**:
   - **APROVADO**: zero bloqueadores encontrados. Lista sugestões opcionais se houver.
   - **REPROVADO**: pelo menos 1 bloqueador encontrado. Lista todos os bloqueadores + indica quem corrige (Carlos ou Diana).

## Output Format

```markdown
# Review Report — [Título da Notícia]
Data: [YYYY-MM-DD]

## Veredito: APROVADO ✅ / REPROVADO ❌

---

## Avaliação de Copy

### Hook
[✅ / ❌] [avaliação em 1-2 linhas]

### Dados
[✅ / ❌] [avaliação — confirma que o dado do copy bate com o news-list.md]

### Estrutura de Slides
[✅ / ❌] [avaliação da sequência e completude dos slides]

### Voz 9Pilla
[✅ / ❌] [avaliação de tom, manifesto, legenda, CTA]

---

## Avaliação de Design

### Legibilidade
[✅ / ❌] [avaliação com fontes e contraste]

### Hierarquia Visual
[✅ / ❌] [avaliação]

### Identidade 9Pilla
[✅ / ❌] [logo, alternância de fundos, acento de cor]

---

## Bloqueadores (se REPROVADO)

1. 🚫 [Descrição específica do bloqueador] → Corrigir com: [Carlos Carrossel / Diana Design]
   **Como corrigir:** [instrução acionável]

---

## Sugestões Opcionais

1. ⚠️ [Sugestão] — impacto esperado: [...]
```

## Output Example

> Referência de qualidade.

```markdown
# Review Report — IPCA-15 Março 2026
Data: 2026-04-07

## Veredito: APROVADO ✅

---

## Avaliação de Copy

### Hook
✅ Hook usa a estrutura "Você sabia que [problema invisível]" — testada e aprovada pela investigação. Conecta imediatamente ao cotidiano do seguidor. Passa no teste de scroll.

### Dados
✅ Dado-chave no copy (+0,44% IPCA-15 março, +3,90% acumulado 12 meses, poupança 6,17% a.a.) confere com o news-list.md da Nara. Fonte primária: IBGE. Nenhuma discrepância identificada.

### Estrutura de Slides
✅ 6 slides na sequência correta: Hook → O que é inflação → Mecanismo global → Poupança vs realidade → Contraste/Solução → CTA. Slide 5 tem estrutura binária → funcionando.

### Voz 9Pilla
✅ Tom educativo-próximo consistente. Manifesto "O problema nunca foi o dinheiro. Foi o acesso à informação." presente no slide 6. Legenda com índice →. CTA para lista de espera 9Pilla presente.

---

## Avaliação de Design

### Legibilidade
✅ Headline mínimo 40px (slide 4 tem 40px — dentro do aceitável). Body mínimo 30px. Contraste adequado em todos os slides.

### Hierarquia Visual
✅ Headline domina em todos os slides. Suporte visivelmente menor e mais claro. Nenhum conflito de hierarquia.

### Identidade 9Pilla
✅ Logo e @9pilla.link no slide 1. Alternância de fundos: escuro → claro → escuro → claro → escuro → escuro (slide 5-6 são ambos escuros — sequência aceitável pois são slides finais com tratamento especial).

---

## Bloqueadores
Nenhum.

---

## Sugestões Opcionais

1. ⚠️ Slide 4 (Poupança vs CDB): o headline está longo (15 palavras). Poderia ser encurtado para "Poupança: 6,17% a.a. CDB: ~10,5%. A conta não fecha." — mais impacto visual em 3 linhas curtas.
2. ⚠️ Legenda: incluir 1 emoji adicional nos bullets → para dar mais escaneabilidade no mobile. Sugestão opcional — não bloqueia.
```

## Quality Criteria

- [ ] Veredito APROVADO/REPROVADO na primeira linha
- [ ] Cada dimensão avaliada com [✅/❌] e justificativa
- [ ] Bloqueadores claramente separados de sugestões opcionais
- [ ] Quando REPROVADO: cada bloqueador tem "Como corrigir" acionável e indica Carlos ou Diana
- [ ] Dados do copy verificados contra news-list.md

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Veredito ausente ou enterrado no meio do texto
2. Bloqueador encontrado mas carrossel marcado como APROVADO
