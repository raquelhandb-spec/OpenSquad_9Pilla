# Mensagem para Turma ou VIP

Cria mensagem para Turma 9Pilla ou Grupo Winner VIP.

## Uso

```bash
/mensagem-grupo <contexto> <destino>
```

## Destinos

- turma (WhatsApp gratuito — comunidade educativa)
- vip (Grupo pago — assinantes ativos)

## Exemplo

```bash
/mensagem-grupo "Copom hoje às 18h - prepare-se para volatilidade" turma
```

## Resultado

Saída: `content/grupos/msg-turma-YYYY-MM-DD.md`

Mensagem:
- **Tone:** Informal, como mensagem de amiga
- **Comprimento:** Máximo 5 linhas
- **Frequência:** Qualidade > quantidade

## Validações

Caio garante:
✓ Tone adequado (mais leve para turma, mais formal para VIP)
✓ Sem exceção: banned words ausentes
✓ CTA claro e direto
✓ Sem spam ou sobrecarregamento

## Fluxo Automático

1. **Nina** (redacao-9pilla) cria mensagem
2. Arquivo salvo em `content/grupos/`

---

**Orquestração via Caio:**
```
node ./.claude/scripts/orchestrator.js mensagem_grupo <contexto> <destino>
  ↓
Nina → Caio
  ↓
Output: content/grupos/msg-[destino]-YYYY-MM-DD.md
```
