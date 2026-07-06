# brapi.dev — Mapa de Endpoints (V2)

Base: `https://brapi.dev/api` · Auth: `Authorization: Bearer ${BRAPI_TOKEN}`
(no-code pode usar `?token=`). Símbolos: `symbols=PETR4,VALE3` (Pro = até 20/req).

## Formato de resposta V2 (IMPORTANTE)
No **V2** o payload de cada ativo fica em **`results[].data`** (diferente do
endpoint **legado** `/api/quote/{ticker}`, onde os campos ficam direto em `results[]`).

```jsonc
{
  "results": [
    {
      "requestedSymbol": "PETR4",
      "symbol": "PETR4",
      "data": {
        "shortName": "PETROBRAS PN",
        "regularMarketPrice": 38.50,
        "regularMarketChangePercent": 0.78,
        "marketCap": 503100000000,
        "logourl": "https://icons.brapi.dev/icons/PETR4.svg"
      }
    }
  ],
  "requestedAt": "2026-06-14T17:08:02.000Z",
  "took": 245
}
```

Períodos contábeis: `period=annual|quarterly`. Modos: `mode=current|history`.
Janela: `startDate`/`endDate` no formato `YYYY-MM-DD`.

## Ações (V2 — recomendado)
| Endpoint | Retorna |
|---|---|
| `GET /api/v2/stocks/quote?symbols=PETR4,VALE3` | Preço, variação, volume, market cap, faixa 52 sem, logo |
| `GET /api/v2/stocks/historical?symbols=PETR4&range=1y&interval=1d` | OHLCV, volume, preço ajustado |
| `GET /api/v2/stocks/dividends?symbols=ITUB4` | Dividendos, JCP, bonificações, subscrições |
| `GET /api/v2/stocks/profile?symbols=PETR4` | CNPJ, setor, indústria, descrição, logo |
| `GET /api/v2/stocks/statistics?symbols=WEGE3&mode=current` | P/L, P/VP, beta, dividend yield, EPS, market cap |
| `GET /api/v2/stocks/financial-data?symbols=WEGE3` | Receita, lucro, EBITDA, margens, dívida, FCL (TTM) |
| `GET /api/v2/stocks/balance-sheet?symbols=PETR4&period=annual` | Ativos, passivos, PL, caixa, dívida |
| `GET /api/v2/stocks/income-statement?symbols=PETR4&period=annual` | DRE |
| `GET /api/v2/stocks/cash-flow?symbols=PETR4&period=annual` | DFC |
| `GET /api/v2/stocks/value-added?symbols=PETR4&period=annual` | DVA |

Legado (ainda suportado): `GET /api/quote/{ticker}?modules=defaultKeyStatistics,...`
Módulos: `summaryProfile`, `balanceSheetHistory(+Quarterly)`, `defaultKeyStatistics(+History+HistoryQuarterly)`,
`incomeStatementHistory(+Quarterly)`, `financialData(+History+HistoryQuarterly)`,
`valueAddedHistory(+Quarterly)`, `cashflowHistory(+Quarterly)`.

## Tickers (descoberta / screener)
| `GET /api/v2/tickers?search=PETR` | Autocomplete/busca |
| `GET /api/v2/tickers/resolve?symbols=VVAR3,PETR4` | Resolver tickers antigos |
| `GET /api/v2/tickers/coverage?symbols=PETR4,MXRF11` | Cobertura por ticker |

## `/api/quote/list` (ranking / filtro) — o "filtrar assuntos"
Params: `sortBy` (name, close, change, change_abs, volume, market_cap_basic, sector),
`sortOrder` (asc|desc), `sector`, `type` (stock|fund|bdr), `search`, `limit`, `page`.
Resposta traz `stocks[]`, `availableSectors`, `availableStockTypes`, paginação.
Ex.: `/api/quote/list?sector=Finance&sortBy=volume&sortOrder=desc&limit=10`

## FIIs
`GET /api/v2/fii/{list|indicators|indicators/history|historical|properties|properties/history|portfolio|portfolio/history|reports|dividends|financials|annual-reports}?symbols=HGLG11`
(inclui vacância em `properties`, rendimentos em `dividends`).

## Outros módulos
- **Fundos** (FI-Infra/FIAGRO/FIDC/FIP): `GET /api/v2/funds/...`
- **Opções**: `GET /api/v2/options/{expirations|strikes|chain|historical|analytics}`
- **Futuros**: `GET /api/v2/futures/{list|quote|specs|historical|term-structure}` (WIN, IND, WDO, DOL, DI1, DAP, BGI, ICF, CCM, SJC)
- **Cripto**: `GET /api/v2/crypto?coin=BTC&currency=BRL` (100+ moedas)
- **Câmbio**: PTAX / `GET /api/v2/currency`
- **Macro**: ver [`02-macro.md`](02-macro.md)
- **MCP p/ IA**: `https://brapi.dev/docs/mcp` · **SDKs**: `npm install brapi` / `pip install brapi`
