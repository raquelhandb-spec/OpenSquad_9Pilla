# Morning Call 9Pilla

Briefings diários de mercado, 09h09 (seg–sex).

## Estrutura

```
morning-call/
├── README.md (este arquivo)
├── template.md
├── 2026-04/
│   ├── 2026-04-15.md
│   ├── 2026-04-14.md
│   └── ...
└── historico.md
```

## Dados obrigatórios

- **IBOV** (índice bovespa)
- **USD** (dólar USDBRL)
- **PETR4** (Petrobras)
- **VALE3** (Vale)
- **ITUB4** (Itaú)

Fonte: **brapi.dev**

## Tom

Raquel conversando com a Turma. Humano, acessível, inspirador. Sem economês.

## Geração

```bash
/morning-call
```

Saída será formatada pronta para Z-API.

---

**Automação:** Make + Z-API (Client-Token no header)
**Frequência:** Seg–sex, 09h09
**Tamanho típico:** 150–200 palavras
