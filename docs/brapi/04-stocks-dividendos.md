# brapi.dev — Dividendos de ações (último provento pago)

Endpoint V2: `GET /api/v2/stocks/dividends?symbols=PETR4`
Params opcionais: `startDate`, `endDate`, `sortBy`, `sortOrder`.
Histórico em **`results[0].data.cashDividends[]`**.

## Campos de cada provento (`cashDividends[]`)
| Campo | Descrição | Exemplo |
|---|---|---|
| `paymentDate` | Data de pagamento | `2026-06-22T03:00:00.000Z` |
| `rate` | Valor por ação (R$) | `0.350486` |
| `label` | Tipo | `DIVIDENDO`, `JCP`, `RENDIMENTO` |
| `lastDatePrior` | Data-com (último dia p/ ter direito) | `2026-06-01T03:00:00.000Z` |
| `approvedOn` | Data de aprovação | `2025-12-11...` ou `null` |
| `isinCode` / `assetIssued` | ISIN do ativo | `BRPETRACNPR6` |

## ⚠️ Armadilha: proventos FUTUROS
`cashDividends[]` inclui proventos **anunciados mas ainda não pagos** (`paymentDate`
no futuro). Para "último provento **pago**", filtre `paymentDate <= hoje` e então
pegue o mais recente. Ordenar por data e pegar o primeiro traz o futuro — errado.

```js
const cash = json.results[0].data.cashDividends;
const nowMs = Date.now();
const ultimoPago = cash
  .filter((d) => new Date(d.paymentDate).getTime() <= nowMs)
  .sort((a, b) => new Date(b.paymentDate) - new Date(a.paymentDate))[0];
// ultimoPago.rate, ultimoPago.paymentDate, ultimoPago.label
```

## Alternativa (snapshot) — endpoint legado
`GET /api/quote/{ticker}?modules=defaultKeyStatistics`
→ `results[0].defaultKeyStatistics.lastDividendValue` + `lastDividendDate`
(um único provento, o último registrado).

## Resumo pro "Ativo do dia"
| O quê | Endpoint | Valor | Data |
|---|---|---|---|
| Snapshot | `/api/quote/{t}?modules=defaultKeyStatistics` | `lastDividendValue` | `lastDividendDate` |
| Histórico | `/api/v2/stocks/dividends?symbols={t}` | `rate` | `paymentDate` |
