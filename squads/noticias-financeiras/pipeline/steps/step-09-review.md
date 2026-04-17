---
execution: inline
agent: squads/noticias-financeiras/agents/rafael-revisao
inputFile: squads/noticias-financeiras/output/slides-report.md
outputFile: squads/noticias-financeiras/output/review-report.md
---

# Step 09: Revisão do Carrossel

## Context Loading

Carregue estes arquivos antes de executar:
- `squads/noticias-financeiras/output/slides-report.md` — design dos slides com link Canva
- `squads/noticias-financeiras/output/carousel-draft.md` — copy completo do carrossel
- `squads/noticias-financeiras/output/news-list.md` — notícias com dados originais (para verificar precisão)
- `squads/noticias-financeiras/pipeline/data/quality-criteria.md` — critérios de qualidade
- `squads/noticias-financeiras/pipeline/data/anti-patterns.md` — erros a evitar

## Instructions

### Process
1. Leia os três inputs: slides-report.md (design), carousel-draft.md (copy), news-list.md (dados originais).
2. Avalie o copy em 4 dimensões: hook, dados, estrutura, voz 9Pilla.
3. Avalie o design em 3 dimensões: legibilidade, hierarquia visual, identidade 9Pilla.
4. Classifique cada achado como 🚫 Bloqueador ou ⚠️ Sugestão.
5. Emita o veredito na primeira linha: APROVADO ou REPROVADO.
6. Se REPROVADO: lista todos os bloqueadores com "Como corrigir" e indica Carlos ou Diana.

## Output Format

```markdown
# Review Report — [Título]
Data: [YYYY-MM-DD]

## Veredito: APROVADO ✅ / REPROVADO ❌

---

## Avaliação de Copy
### Hook [✅/❌] [avaliação]
### Dados [✅/❌] [avaliação + verificação contra news-list.md]
### Estrutura [✅/❌] [avaliação]
### Voz 9Pilla [✅/❌] [avaliação]

---

## Avaliação de Design
### Legibilidade [✅/❌] [avaliação]
### Hierarquia Visual [✅/❌] [avaliação]
### Identidade 9Pilla [✅/❌] [avaliação]

---

## Bloqueadores (se REPROVADO)
1. 🚫 [descrição] → Corrigir com: [Carlos/Diana]
   **Como corrigir:** [instrução acionável]

---

## Sugestões Opcionais
1. ⚠️ [sugestão] — impacto esperado: [...]
```

## Output Example

```markdown
# Review Report — IPCA-15 Março 2026
Data: 2026-04-07

## Veredito: APROVADO ✅

---

## Avaliação de Copy
### Hook ✅
Usa a estrutura "Problema Invisível" — testada na investigação. Conecta ao cotidiano imediatamente. Passa no teste de scroll.

### Dados ✅
Dado-chave (+0,44%, +3,90% acumulado, poupança 6,17%, passagem +5,94%) confere com news-list.md da Nara. Fonte primária IBGE confirmada.

### Estrutura ✅
6 slides na sequência correta: Hook → Inflação → Mecanismo → Poupança → Contraste → CTA. Slide 5 com binário → funcionando.

### Voz 9Pilla ✅
Tom educativo-próximo consistente. Manifesto presente no slide 6. Legenda com índice →. CTA claro para a turma 9Pilla.

---

## Avaliação de Design
### Legibilidade ✅
Headline mínimo 43px. Body mínimo 32px. Contraste adequado em todos os slides.

### Hierarquia Visual ✅
Headline dominante em todos os slides. Suporte visivelmente secundário.

### Identidade 9Pilla ✅
Logo e @9pilla.link no slide 1. Alternância de fundos adequada. Acento de cor consistente.

---

## Bloqueadores
Nenhum.

---

## Sugestões Opcionais
1. ⚠️ Slide 4: headline com 15 palavras — poderia ser mais curto para maior impacto visual.
```

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Veredito ausente ou não está na primeira linha
2. Bloqueador encontrado mas carrossel marcado APROVADO

## Quality Criteria

- [ ] Veredito na primeira linha
- [ ] Todas as 7 dimensões avaliadas (4 copy + 3 design)
- [ ] Dados verificados contra news-list.md
- [ ] Bloqueadores separados de sugestões opcionais
