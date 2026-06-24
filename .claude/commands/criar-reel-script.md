# Criar Script de Reel

Cria um script completo de Reel em 6 slides para Instagram/TikTok.

## Uso

```bash
/criar-reel-script <tema>
```

## Exemplo

```bash
/criar-reel-script "Como investir em ações com pouco dinheiro"
```

## Resultado

Saída: `content/reels/reel-YYYY-MM-DD.md`

Contém:
- Slide 1: Hook (sem palavras banidas)
- Slides 2-5: Desenvolvimento com layout + texto na tela + narração HeyGen
- Slide 6: CTA para Turma 9Pilla

Cada slide tem máximo 15 segundos de narração.

## Fluxo Automático

1. **Nina** (redacao-9pilla) cria roteiro
2. **Léa** (checklist-cvm) valida compliance
3. Arquivo salvo em `content/reels/`

## Próximos Passos

Após criação:
1. Revisar em `content/reels/reel-YYYY-MM-DD.md`
2. Exportar para Canva
3. Adicionar narração HeyGen (avatar + voz Raquel)
4. Editar em CapCut Pro
5. Publicar no Instagram

---

**Orquestração via Caio:**
```
node ./.claude/scripts/orchestrator.js criar_reel_script <tema>
  ↓
Nina → Léa → Caio
  ↓
Output: content/reels/reel-YYYY-MM-DD.md
```
