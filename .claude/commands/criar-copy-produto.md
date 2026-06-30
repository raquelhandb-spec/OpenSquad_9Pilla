# Criar Copy de Produto

Gera copy de venda para produto 9Pilla com Voice DNA da Raquel.

## Uso

```bash
/criar-copy-produto <produto> <canal>
```

## Produtos Disponíveis

- "Ebook Diário de Operações" (R$ 49,90 | com cupom: R$ 29,90)
- "Grupo Winner VIP" (assinatura recorrente)
- "Mentoria 1:1" (R$ 5.000 | com desconto: R$ 3.799)

## Canais

- instagram
- whatsapp
- email

## Exemplo

```bash
/criar-copy-produto "Ebook Diário de Operações" instagram
```

## Resultado

Saída: `content/copies/copy-YYYY-MM-DD-ebook.md`

Contém:
- Benefício = entendimento + autonomia (NUNCA lucro garantido)
- Prova social
- Urgência real (NUNCA fake)
- CTA direto com link/WhatsApp

## Validações

Caio garante:
✓ Nenhuma promessa de retorno
✓ Nenhuma recomendação específica de ativo
✓ Disclaimer CVM presente (se necessário)
✓ Voice DNA de Raquel coerente
✓ Banned words ausentes

## Fluxo Automático

1. **Nina** (redacao-9pilla) cria copy
2. **Léa** (checklist-cvm) valida compliance
3. Arquivo salvo em `content/copies/`

---

**Orquestração via Caio:**
```
node ./.claude/scripts/orchestrator.js criar_copy_produto <produto> <canal>
  ↓
Nina → Léa → Caio
  ↓
Output: content/copies/copy-YYYY-MM-DD-[produto].md
```
