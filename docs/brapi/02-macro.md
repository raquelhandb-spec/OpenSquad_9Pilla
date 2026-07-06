# brapi.dev — Módulo Macro (SELIC, CDI, IPCA…)

Plano: `/api/v2/macro` requer plano pago (Startup/Pro) ✅. `/api/v2/macro/available` é público.

## Endpoints
```
GET /api/v2/macro/available            # descobrir séries (filtros: ?q=juros&category=interestRate)
GET /api/v2/macro/latest?symbols=selic,cdi,ipca                 # valores mais recentes
GET /api/v2/macro?symbols=ipca&startDate=2025-01-01&endDate=2026-07-06&sortOrder=desc&limit=20   # histórico
```

## Formato de resposta
Cada série vem em `results[]`, identificada por `results[].series.slug`
(`selic`, `cdi`, `ipca`), com os pontos em `results[].observations[].{date,value}`.

```jsonc
{
  "results": [
    {
      "series": { "slug": "selic", "name": "Taxa Selic", "unit": "percentPerYear",
                  "frequency": "daily", "category": "interestRate" },
      "observations": [ { "date": "2026-07-03", "value": 14.75 } ]
    },
    {
      "series": { "slug": "ipca", "name": "IPCA", "unit": "percentPerMonth",
                  "frequency": "monthly", "category": "inflation" },
      "observations": [ { "date": "2026-06-01", "value": 0.32 },
                        { "date": "2026-05-01", "value": 0.41 } ]
    }
  ]
}
```

Notas de unidade:
- `selic` e `cdi`: `percentPerYear` (ex.: 14,75% a.a.). CDI ≈ Selic − 0,10 a.a.
- `ipca`: `percentPerMonth` (mensal). Para 12 meses, junte os últimos 12.

## Juro real (linha de ouro do Morning Call)
IPCA acumulado 12m — o correto é **compor**, não somar:
```js
const ipca12m = (mensais12.reduce((acc, v) => acc * (1 + v / 100), 1) - 1) * 100;
const juroReal = ((1 + selic / 100) / (1 + ipca12m / 100) - 1) * 100;
// Ex.: Selic 14,75% e IPCA 12m 4,50% → juro real ≈ 9,81% a.a.
```
