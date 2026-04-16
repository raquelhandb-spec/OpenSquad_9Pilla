# /campanha

Acessa o sistema de campanha da **Turma 9Pilla** (grupo WhatsApp gratuito).

## Estrutura da Turma 9Pilla

**Nome:** Turma 9Pilla  
**JID:** `120363407926604570-group`  
**Tipo:** Grupo aberto (lead magnet)  
**Objetivo:** Educação financeira, aquecimento, funil para Panelinha Secreta  
**Tamanho:** [X] membros  

## Automações ativas

### 1. Morning Call (09h09 seg–sex)

- **O quê:** Briefing diário de mercado (IBOV, USD, ações principais)
- **Quem envia:** Make + Z-API (Client-Token no header)
- **Frequência:** Seg–sex, 09h09
- **Objetivo:** Criar hábito, valor diário, retenção

### 2. Bem-vindo (novo membro)

- **O quê:** Mensagem de acolhimento + EP.01 "Papo de Grana"
- **Quem envia:** Z-API / ManyChat
- **Trigger:** Membro entra no grupo
- **Objetivo:** Educação imediata, qualificação

### 3. Conteúdo programado

- **O quê:** Trechos de "Papo de Grana" (episódios)
- **Quando:** [Dia/Hora TBD]
- **Objetivo:** Nutrição constante

## Métricas

- **Crescimento:** [X] novos membros/semana
- **Retenção:** [Y]%
- **Conversão → Panelinha:** [Z]%
- **Engajamento:** Reações, respostas, forward

## Comando

```
/campanha [ação]
```

Ações disponíveis:

| Ação | Descrição |
|------|-----------|
| `status` | Mostra saúde atual da Turma |
| `metricas` | Últimas 7 dias (crescimento, retenção) |
| `enviar` | Compõe e envia mensagem para a Turma |
| `agendado` | Lista mensagens agendadas |
| `novo-fluxo` | Cria novo fluxo de automação |

## Exemplo

```
/campanha status
```

Saída:

```
📊 Turma 9Pilla — Status

✅ Ativa  
👥 Membros: 2.847 (↑ 8% semana)  
💬 Morning Call: 09h09 (prox. amanhã)  
📚 Bem-vindo: automático  
⏰ Próximo conteúdo: [data]

🎯 Funil para Panelinha Secreta  
Conversão: 2.3% (meta: 5%)
```

## Gerenciamento

Raquel tem acesso direto via:
- **WhatsApp:** Admin do grupo
- **Make:** Conta com acesso a workflows
- **Z-API:** Admin da integração (Client-Token)

---

**Pendência:** Escalabilidade do funil (aumentar conversão para Panelinha Secreta)
