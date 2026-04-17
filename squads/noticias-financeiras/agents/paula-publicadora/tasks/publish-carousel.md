---
task: "Publish Carousel"
order: 1
input: |
  - carousel_draft: Copy completo com legenda final (carousel-draft.md)
  - slides_report: Link Canva com as imagens (slides-report.md)
output: |
  - publish_report: URL do post publicado, post ID, timestamp, status
---

# Publish Carousel

Executa a publicação do carrossel aprovado no Instagram da 9Pilla usando o instagram-publisher.

## Process

1. **Verifica a aprovação da Gabi Gatilho** no `review-report.md` e no output do step-10. Se não houver confirmação "sim" registrada, para imediatamente e reporta.

2. **Extrai a caption** do `carousel-draft.md` — seção LEGENDA. Verifica que tem ≤ 2.200 caracteres.

3. **Acessa o Canva** via link do `slides-report.md` e exporta todos os slides como JPEG 1080x1440px. Salva em `squads/noticias-financeiras/output/images/` com nomes sequenciais: `slide-01.jpg`, `slide-02.jpg`, etc.

4. **Verifica os requisitos técnicos**:
   - [ ] Todas as imagens em formato JPEG
   - [ ] Entre 2 e 10 imagens
   - [ ] Caption ≤ 2.200 caracteres
   - Se qualquer verificação falhar, reporta o problema e para.

5. **Executa o script de publicação**:
   ```
   node --env-file=.env squads/noticias-financeiras/../../skills/instagram-publisher/scripts/publish.js \
     --images "output/images/slide-01.jpg,output/images/slide-02.jpg,..." \
     --caption "<caption>"
   ```
   Adiciona `--dry-run` se o usuário tiver solicitado teste sem publicação real.

6. **Registra o resultado** no output e atualiza o `runs.md` da squad.

## Output Format

```markdown
# Publish Report — [Título da Notícia]
Data: [YYYY-MM-DD HH:MM]
Status: PUBLICADO ✅ / FALHA ❌ / DRY-RUN 🧪

---

## Resultado

**Post URL:** [https://www.instagram.com/p/XXXXXX/]
**Post ID:** [ID retornado pela API]
**Timestamp:** [YYYY-MM-DD HH:MM:SS]
**Imagens publicadas:** [N] slides
**Caption:** [primeiros 125 caracteres...]

---

## Detalhes Técnicos

- Imagens: [lista de arquivos]
- Caption: [N] caracteres (limite: 2.200)
- Conta: @9pilla.link
- Modo: [publicação real / dry-run]

---

## Erro (se FALHA)

**Código:** [código de erro da API]
**Mensagem:** [mensagem de erro completa]
**Causa provável:** [token expirado / rate limit / formato de imagem / outro]
**Solução:** [passo a passo para resolver]
```

## Output Example

> Referência de qualidade.

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

- Imagens: slide-01.jpg a slide-06.jpg (6 arquivos, JPEG 1080x1440px)
- Caption: 847 caracteres (limite: 2.200)
- Conta: @9pilla.link
- Modo: publicação real

---

## Histórico Atualizado

runs.md atualizado com esta publicação.
```

## Quality Criteria

- [ ] Aprovação da Gabi Gatilho verificada antes de executar
- [ ] Caption extraída do carousel-draft.md (não reescrita)
- [ ] Imagens em JPEG, entre 2-10 slides
- [ ] URL do post publicado no output
- [ ] runs.md atualizado

## Veto Conditions

Rejeita e não publica se QUALQUER uma for verdadeira:
1. Nenhuma confirmação "sim" encontrada no output da Gabi Gatilho
2. Imagens não estão em formato JPEG ou estão fora do range 2-10
