# 🤖 Bot de Aprovação: Como Usar (SUPER SIMPLES)

**Para:** Raquel
**Atualizado:** 11/06/2026

---

## Por que o bot não respondia antes?

Um bot tem 2 partes:
1. **Enviar mensagem** (isso funcionava)
2. **Escutar seus cliques** (isso NÃO EXISTIA, nenhum programa rodando!)

Quando você apertou 👎, ninguém estava ouvindo. Agora existe o
`approval_bot.py`, o programa que faltava. E trocamos reação de emoji
por **BOTÕES** na mensagem, muito mais confiável.

---

## Como usar (2 passos no seu Windows)

### Passo 1: Baixar o código atualizado

Abra o **cmd** e rode:

```
cd C:\caminho\para\OpenSquad_9Pilla
git pull origin claude/moneprinter-9pilla-integration-9gm87x
```

*(Se você ainda não tem a pasta, me chama que te guio no clone)*

### Passo 2: Ligar o bot

```
cd squads\shorts-maestro
python approval_bot.py
```

Vai aparecer:

```
🤖 BOT DE APROVAÇÃO 9PILLA — ESCUTANDO
   Deixe esta janela ABERTA. Ctrl+C para parar.
```

**Deixe essa janela aberta!** Enquanto ela estiver aberta, o bot responde
seus cliques NA HORA.

---

## Testar agora (opcional)

Em OUTRA janela do cmd:

```
cd squads\shorts-maestro
python approval_bot.py --send-test
```

Isso envia o último script aprovado para o seu Telegram **com botões**.
Aí você clica em ✅ ou ❌ e vê o bot responder na hora!

---

## O que acontece quando você clica

| Botão | Resposta do bot | O que é salvo |
|-------|----------------|---------------|
| ✅ APROVAR | "Aprovado! Gerando vídeo..." | `data/approvals/{id}.json` → approved |
| ❌ REJEITAR | "Rejeitado, zero gasto! Me conta o que não gostou?" | rejected |
| (responder texto após rejeitar) | "Feedback anotado!" | seu feedback fica salvo |

O orchestrator lê essas decisões para liberar (ou não) o HeyGen.
**Rejeição = zero gasto, sempre.**

---

## Comandos úteis no chat do Telegram

- `/start` → confirma que o bot está vivo
- `/status` → mostra quantas decisões já foram registradas
