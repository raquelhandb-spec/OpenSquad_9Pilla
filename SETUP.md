# Setup 9Pilla · OpenSquad

**Data:** Abr/15/2026  
**Status:** ⚙️ Em construção

## ✅ Concluído

### Infraestrutura

- [x] Diretório `.claude/` criado
- [x] `settings.json` configurado (permissões, MCP servers, hooks)
- [x] `.claude/commands/` estruturado com 5 comandos:
  - [x] `/morning-call` — briefing diário
  - [x] `/novo-ep` — estrutura episódios Papo de Grana
  - [x] `/reel` — gerador de roteiros Reel Instagram
  - [x] `/auditoria-ig` — análise de performance Instagram
  - [x] `/campanha` — gerenciamento Turma 9Pilla

### Estrutura de conteúdo

- [x] `content/morning-call/` + README
- [x] `content/papo-de-grana/` + README (episódios EP.01–EP.09)
- [x] `content/instagram/` + README (Reels, Carrosséis, Stories)
- [x] `assets/brand/` + BRAND.md + cores.json
- [x] `assets/templates/` (pronto para Canva)

### Brand & Identidade

- [x] Cores definidas (Orange #E84A1E, Dark #1C2E1F, Beige, Sand)
- [x] Tipografia documentada (Lora, DM Sans, Caveat)
- [x] Tom de voz fixo (Organic Intel)
- [x] Tagline aprovada: *"Liberdade não se aposenta. Se constrói todo dia."*

## 🔄 Em progresso

- [ ] Paperclip AI (`npx paperclipai onboard --yes`) — instalando...
- [ ] Verificar `.claude/settings.json` após Paperclip
- [ ] Configurar MCP servers (Gmail, Google Calendar)

## 📋 Próximos passos (Prioridade)

### Imediato (Esta semana)

1. **Paperclip finalizar instalação**
   - Confirmar integração com Claude Code
   - Testar orquestração de agentes

2. **Validar comandos funcionam**
   ```bash
   /morning-call
   /novo-ep 02
   /reel radiografia
   /auditoria-ig
   /campanha status
   ```

3. **Criar Morning Call de amanhã (Abr/16)**
   - Coletar dados brapi.dev
   - Roteiro pronto em 10 min
   - Teste Z-API (Client-Token no header)

### Curto prazo (Próximas 2 semanas)

4. **Produzir EP.02 "O medo por trás de cada centavo"**
   - Estrutura: 25k–35k palavras
   - Neurociência + comportamento
   - Mínimo 3 fontes por seção
   - Revisão qualidade

5. **Escalar Instagram (57/100 → 70/100)**
   - Gerar 3 Reels/semana (pilares balanceados)
   - Carrossél semanal (Tesouro Direto, ações, etc.)
   - Monitorar conversão comentário → WhatsApp

6. **Validar funil Turma 9Pilla → Panelinha Secreta**
   - Métrica: conversão atual
   - Teste de fluxo automático ManyChat
   - Aumentar para 5%+

### Médio prazo (Até Maio)

7. **Produzir EP.03–EP.09** (2–3 episódios/mês)
   - Manter padrão de qualidade
   - Neurociência + dados + acessibilidade
   - Distribuir na Turma 9Pilla

8. **Escalar Morning Call**
   - Adicionar análise macro (contexto econômico)
   - Ingestão automática de dados de mercado
   - Integração Notion para histórico

9. **Atingir 80/100 no Instagram**
   - Crescimento consistente
   - Melhor ROI de conteúdo
   - Funil otimizado

## 🎯 Métricas-chave

| Métrica | Atual | Meta | Prazo |
|---------|-------|------|-------|
| Seguidores Instagram | [TBD] | 5.000+ | Maio |
| Engajamento Instagram | 57/100 | 80/100 | Maio |
| Membros Turma 9Pilla | [TBD] | +30% | Maio |
| Conversão → Panelinha | [TBD] | 5%+ | Junho |
| EP Papo de Grana | 1/9 | 3/9 | Maio |

## 📂 Estrutura final

```
OpenSquad_9Pilla/
├── CLAUDE.md ← Instruções (NUNCA ALTERAR)
├── SETUP.md ← Este arquivo
├── .claude/
│   ├── settings.json
│   ├── settings.local.json
│   └── commands/
│       ├── morning-call.md
│       ├── novo-ep.md
│       ├── reel.md
│       ├── auditoria-ig.md
│       └── campanha.md
├── content/
│   ├── morning-call/
│   ├── papo-de-grana/
│   └── instagram/
├── app/ ← 9Pilla APP (GitHub Pages)
└── assets/
    ├── brand/
    └── templates/
```

---

**Última atualização:** Abr/15/2026, 20:XX  
**Próxima revisão:** Abr/22/2026
