# /morning-call

Gera o briefing diário de mercado para o Morning Call 9Pilla (09h09).

## Fluxo

1. **Coleta de dados** → brapi.dev (IBOV, USD, PETR4, VALE3, ITUB4)
2. **Análise** → contexto econômico, oportunidades, riscos
3. **Tom** → Raquel conversando com a Turma, sem economês
4. **Formato** → texto WhatsApp ~150–200 palavras
5. **Saída** → pronto para copiar/colar no Z-API

## Dados obrigatórios

- **IBOV** — Índice Bovespa (abertura, fechamento, variação %)
- **USD** — Dólar USDBRL (preço, variação)
- **PETR4** — Petrobras (preço, variação)
- **VALE3** — Vale (preço, variação)
- **ITUB4** — Itaú (preço, variação)

## Tom e estrutura

**Abertura:** Humanização, conexão emocional  
**Meio:** Dados + contexto (o que significa para o portfólio)  
**Encerramento:** Ação concreta ou reflexão

## Exemplo

```
Bom dia, turma! 🌅

Abr/15 — IBOV abriu em alta de 0,8%. Dólar caindo (R$ 4,92), PETR4 sobe 1,2%, VALE3 estável. 

A real: mercado respirou fundo. Se você tá em renda fixa, aproveita as taxas altas *agora*. Se tá em ações, lembrete: volatilidade é preço da entrada.

Sua ação do dia?
— Revisar sua alocação
— Adicionar em cotas de fundo
— Só deixar rodar

Qual é a sua, pillinha?

9Pilla · Liberdade não se aposenta 🌱
```

## Comando

Use:
```
/morning-call
```

Saída será formatada pronta para Z-API (grupo Turma-9Pilla).

---

**Automação:** Disparo automático seg–sex às 09h09 via Make + Z-API (Client-Token no header, não na URL)
