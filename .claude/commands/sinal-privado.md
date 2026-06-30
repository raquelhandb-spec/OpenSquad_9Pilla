# Sinal Privado

Gera sinal ITM exclusivo para Raquel (NUNCA publicar em canal público).

## ⚠️ RESTRIÇÃO CRÍTICA

**Este comando é RESTRITO.** Output deve ir APENAS para Raquel via canal privado.

Publicar em canal público = violação de compliance CVM.

## Uso

```bash
/sinal-privado <ativo> <tipo>
```

## Ativos Suportados

- PETR4 (ações)
- VALE3 (ações)
- BOVA11 (ETF)
- Índice Futuro

## Tipos de Sinal

- call (alta)
- put (baixa)

## Exemplo

```bash
/sinal-privado PETR4 call
```

## Resultado

**Output:** APENAS para Raquel (celular/privado)

Contém:
- Strike específico
- Direção (Call/Put)
- Prazo
- Razão técnica
- Risco/Reward

**Formato:**
```
🚨 SINAL PRIVADO - RAQUEL ONLY

Setup: PETR4 Call 39,00
Prazo: 8 dias
Técnica: Suporte quebrado em 38,50; reteste hoje provável
Risco: Suporte cai para 37,80
Reward: Alvo 40,50 (+3,8%)

Validar antes de entrar. Volatilidade implícita em nível alto.
```

## Validações (CRÍTICAS)

Caio + Léa garantem:
✓ Sinal é APENAS para Raquel
✓ Nunca vai para Turma/VIP/Instagram
✓ Arquivo salvo em `content/sinais/` (private only)
✓ Setup técnico é válido
✓ Não há recomendação direta (educativo)

## Fluxo Automático

1. **Amorim** (editor) analisa e gera sinal
2. **Léa** (checklist-cvm) valida: "É PRIVADO?"
3. Arquivo salvo em `content/sinais/`
4. ⚠️ BLOQUEIO AUTOMÁTICO se houver risco de publicação pública

---

**Orquestração via Caio:**
```
node ./.claude/scripts/orchestrator.js sinal_privado <ativo> <tipo>
  ↓
Amorim → Léa (validação privada) → Caio
  ↓
Output: content/sinais/sinal-RAQUEL-ONLY-YYYY-MM-DD.md
        ⚠️ NUNCA publicar em canal público
```

## Responsabilidade Legal

Léa é responsável por garantir que nenhum sinal escape para público.

Uma aprovação de Léa significa:
- ✅ Conteúdo é PRIVADO
- ✅ Destinado APENAS a Raquel
- ✅ Compliance CVM garantido
