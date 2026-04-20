# 🎯 Squad Prospecting — Turma 9Pilla

**Missão:** Encontrar pessoas com dor financeira em plataformas públicas e convidá-las para a Turma 9Pilla (grupo gratuito).

**CTA:** https://chat.whatsapp.com/Ly0K34qNxdT75boi9g4eOF

---

## Estrutura da Esteira

```
[M1] YouTube ──┐
[M2] Reddit ───┼──→ leads_pool.json → [Q] Qualificador → [C] Copywriter → abordagens_prontas.md
[M3] LinkedIn ─┤
[M4] Instagram ┘
```

## Agentes

| ID | Nome | Função | Plataforma |
|----|------|---------|------------|
| M1 | Minerador YouTube | Garimpa comentários com dor | YouTube |
| M2 | Minerador Reddit | Garimpa posts/comentários | Reddit |
| M3 | Minerador LinkedIn | Garimpa perfis e posts | LinkedIn |
| M4 | Minerador Instagram | Garimpa comentários | Instagram |
| Q1 | Qualificador | Classifica 🔥/🟡/❄️ | — |
| C1 | Copywriter Raquel | Escreve abordagem personalizada | — |
| CEO | CEO-9Pilla | Revisa, aprova, monitora | — |

## Como Rodar

```bash
# Rodar todos os mineradores (faz busca em paralelo)
gemini < squads/prospecting/run-mineradores.md

# Qualificar leads encontrados
gemini < squads/prospecting/run-qualificador.md

# Gerar abordagens prontas
gemini < squads/prospecting/run-copywriter.md
```
