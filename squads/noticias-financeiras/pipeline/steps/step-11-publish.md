---
execution: subagent
agent: squads/noticias-financeiras/agents/paula-publicadora
inputFile: squads/noticias-financeiras/output/carousel-draft.md
outputFile: squads/noticias-financeiras/output/publish-report.md
model_tier: fast
---

# Step 11: Publicação no Instagram

## Context Loading

Carregue estes arquivos antes de executar:
- `squads/noticias-financeiras/output/carousel-draft.md` — legenda final do carrossel
- `squads/noticias-financeiras/output/slides-report.md` — link do Canva para download das imagens
- `squads/noticias-financeiras/output/review-report.md` — confirmar que tem veredito APROVADO
- `squads/noticias-financeiras/skills/instagram-publisher/SKILL.md` — instruções de uso do publisher

## Instructions

### Process
1. Verifique que o step-10 retornou "sim" do usuário. Se não, pare imediatamente.
2. Extraia a legenda completa do `carousel-draft.md` — seção LEGENDA. Verifique: ≤ 2.200 caracteres.
3. Acesse o link do Canva do `slides-report.md` e exporte todos os slides como JPEG 1080x1440px. Salve em `output/images/` com nomes `slide-01.jpg`, `slide-02.jpg`, etc.
4. Verifique os requisitos: imagens JPEG, entre 2 e 10 slides.
5. Execute o script de publicação usando o instagram-publisher (conforme SKILL.md).
6. Salve a URL do post publicado e o post ID no output.
7. Atualize o `_memory/runs.md` da squad com os dados desta execução.

## Output Format

```markdown
# Publish Report — [Título]
Data: [YYYY-MM-DD HH:MM]
Status: PUBLICADO ✅ / FALHA ❌ / DRY-RUN 🧪

---

## Resultado
**Post URL:** [https://www.instagram.com/p/XXXXXX/]
**Post ID:** [ID]
**Timestamp:** [YYYY-MM-DD HH:MM:SS]
**Imagens publicadas:** [N] slides
**Caption:** [primeiros 125 chars...]

---

## Detalhes Técnicos
- Imagens: [lista de arquivos]
- Caption: [N] caracteres
- Conta: @9pilla.link
- Modo: [real / dry-run]

---

## Erro (se FALHA)
**Código:** [código]
**Mensagem:** [mensagem completa]
**Causa:** [token expirado / rate limit / formato / outro]
**Solução:** [passos para resolver]
```

## Output Example

```markdown
# Publish Report — IPCA-15 Março 2026
Data: 2026-04-07 14:32
Status: PUBLICADO ✅

---

## Resultado
**Post URL:** https://www.instagram.com/p/DXa1B2cDefG/
**Post ID:** 17841234567890123
**Timestamp:** 2026-04-07 14:32:45
**Imagens publicadas:** 6 slides
**Caption:** "Seu dinheiro está perdendo valor todos os meses — mesmo sem você gastar mais..."

---

## Detalhes Técnicos
- Imagens: slide-01.jpg a slide-06.jpg (JPEG 1080x1440px)
- Caption: 847 caracteres
- Conta: @9pilla.link
- Modo: publicação real
```

## Veto Conditions

Para e não publica se QUALQUER uma for verdadeira:
1. Nenhuma confirmação "sim" verificada no output do step-10
2. Imagens não são JPEG ou estão fora do range 2-10

## Quality Criteria

- [ ] Confirmação do step-10 verificada antes de executar
- [ ] Caption extraída do carousel-draft.md sem reescrita
- [ ] Imagens exportadas em JPEG
- [ ] URL do post publicado no output
- [ ] runs.md atualizado
