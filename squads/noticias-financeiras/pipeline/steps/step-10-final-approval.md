---
execution: inline
agent: squads/noticias-financeiras/agents/gabi-gatilho
inputFile: squads/noticias-financeiras/output/review-report.md
---

# Step 10: Aprovação Final para Publicação

## Context Loading

Carregue estes arquivos antes de executar:
- `squads/noticias-financeiras/output/review-report.md` — resultado da revisão do Rafael
- `squads/noticias-financeiras/output/carousel-draft.md` — para extrair o hook do slide 1
- `squads/noticias-financeiras/output/slides-report.md` — para extrair o link do Canva

## Instructions

### Process
1. Confirme que o review-report.md tem veredito APROVADO. Se for REPROVADO, pare e informe o usuário — o pipeline retorna ao step-06.
2. Extraia do carousel-draft.md: o hook do slide 1 e os primeiros 125 caracteres da legenda.
3. Extraia do slides-report.md: o link do Canva.
4. Monte o resumo em no máximo 10 linhas.
5. Apresente a pergunta de aprovação em destaque.
6. Aguarde resposta explícita "sim". Qualquer outra resposta pausa o pipeline.

## Output Format

```markdown
# Resumo para Aprovação

📰 **Notícia:** [título da notícia]
🎯 **Ângulo:** [nome do ângulo]
🎨 **Tom:** [tom usado]
📱 **Slides:** [N] slides
📝 **Hook:** "[primeira linha do slide 1]"
🔗 **Design:** [link Canva]
✅ **Revisão:** Aprovado pelo Rafael Revisão — sem bloqueadores

---

**Posso publicar? (responda "sim" para publicar)**
```

## Output Example

```markdown
# Resumo para Aprovação

📰 **Notícia:** IPCA-15 de março sobe 0,44%, acima das expectativas
🎯 **Ângulo:** Problema Invisível
🎨 **Tom:** Educativo-Próximo
📱 **Slides:** 6 slides
📝 **Hook:** "Seu dinheiro está perdendo valor — mesmo sem você gastar mais"
🔗 **Design:** https://www.canva.com/design/DAxxxxxx/view
✅ **Revisão:** Aprovado pelo Rafael Revisão — sem bloqueadores

---

**Posso publicar? (responda "sim" para publicar)**
```

## Veto Conditions

Para o pipeline imediatamente se QUALQUER uma for verdadeira:
1. review-report.md tem veredito REPROVADO — retorna ao step-06 com os bloqueadores do Rafael
2. Usuário não responde "sim" (resposta diferente, silêncio, "talvez") — aguarda ou retorna conforme instrução do usuário

## Quality Criteria

- [ ] Resumo com ≤ 10 linhas
- [ ] Inclui: notícia, ângulo, hook, link Canva, resultado da revisão
- [ ] Pergunta "Posso publicar?" em destaque
- [ ] Não avança para step-11 sem "sim" explícito
