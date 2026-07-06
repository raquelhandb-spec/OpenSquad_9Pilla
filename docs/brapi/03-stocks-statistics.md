# brapi.dev — Estatísticas / Fundamentos por ação

Endpoint: `GET /api/v2/stocks/statistics?symbols=PETR4`
Params: `symbols` (até 20), `mode=current` (padrão) ou `mode=history&period=quarterly`.
Payload em **`results[0].data`** (padrão V2).

## Campos usados no "Ativo do dia"
| Campo (V2 `data.`) | Label | Observação |
|---|---|---|
| `dividendYield` | Dividend Yield | **decimal** → ×100 (0.1399 = 13,99%) |
| `trailingPE` | P/L (12m) | no **legado** o nome é `priceEarnings` |
| `forwardPE` | P/L futuro | |
| `priceToBook` | P/VP | |
| `marketCap` | Valor de mercado | em R$ |
| `beta` | Beta | volatilidade vs mercado |
| `lastDividendValue` | Último dividendo | R$ |
| `lastDividendDate` | Data último dividendo | `YYYY-MM-DD` |
| `earningsPerShare` / `trailingEps` | LPA | |
| `profitMargins` | Margem líquida | decimal |
| `enterpriseValue`, `enterpriseToEbitda` | EV, EV/EBITDA | |

ROE (`returnOnEquity`) vem via `/api/v2/stocks/financial-data`.

## Mapeamento V2 × Legado (pra fallback)
| Indicador | V2 (`statistics`) | Legado (`quote?modules=defaultKeyStatistics`) |
|---|---|---|
| Dividend Yield | `results[0].data.dividendYield` | `results[0].defaultKeyStatistics.dividendYield` |
| P/L | `results[0].data.trailingPE` | `results[0].defaultKeyStatistics.priceEarnings` |

## Exemplo de resposta
```jsonc
{
  "results": [
    {
      "symbol": "PETR4",
      "data": {
        "dividendYield": 0.1399, "trailingPE": 5.24, "forwardPE": 5.89,
        "priceToBook": 1.52, "marketCap": 468500000000, "beta": 0.94,
        "lastDividendValue": 0.94, "lastDividendDate": "2026-05-15",
        "earningsPerShare": 8.42, "trailingEps": 7.91, "profitMargins": 0.22
      }
    }
  ]
}
```

## Dividendos detalhados
`GET /api/v2/stocks/dividends?symbols=ITUB4` → histórico de dividendos, JCP,
bonificações e subscrições (para "quanto pagou nos últimos 12 meses").
