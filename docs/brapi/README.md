# Documentação brapi.dev — referência offline da 9Pilla

> **Por que esta pasta existe:** o site `brapi.dev` está bloqueado no ambiente
> de execução do Claude (proxy da rede). Guardando a documentação aqui, o Claude
> consegue **consultar os endpoints, os campos e os formatos de resposta direto
> do repositório**, sem depender de acesso à internet. Esta pasta é a "fonte da
> verdade" do brapi para o projeto 9Pilla.

Plano contratado: **Pro** (R$ 99,99/mês) → 500 mil req/mês, delay ~5 min,
fundamentos completos, dividendos, FIIs, macro, ranking `/quote/list`.

Autenticação: header `Authorization: Bearer ${BRAPI_TOKEN}` (secret no GitHub).
Base URL: `https://brapi.dev/api`.

## Índice

| Arquivo | Conteúdo |
|---|---|
| [`01-endpoints-overview.md`](01-endpoints-overview.md) | Mapa geral dos endpoints (ações V2, FIIs, fundos, opções, futuros, tickers) + formato de resposta V2 |
| [`02-macro.md`](02-macro.md) | Módulo macro (SELIC, CDI, IPCA…) + cálculo do juro real |
| [`03-stocks-statistics.md`](03-stocks-statistics.md) | Estatísticas e fundamentos por ação (DY, P/L, último provento…) |

## Regra de ouro do projeto
**Dado real ou nada.** Nenhum número "plausível" entra no conteúdo. Se a fonte
não confirmar, o pipeline aborta (ver `.claude/scripts/lib/market-data.js`).
