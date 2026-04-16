#!/bin/bash

# 🌅 Script de Ativação - Morning Call Automático
# Ativa a rotina no Paperclip com um comando

echo "🚀 Ativando Morning Call Automático..."
echo ""

# Verificar se Paperclip está instalado
if ! command -v npx &> /dev/null; then
    echo "❌ NPX não encontrado. Instale Node.js e npm."
    exit 1
fi

echo "📋 Verificando testes..."
node .claude/scripts/test-morning-call.js

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Existem problemas. Corrija-os antes de ativar."
    exit 1
fi

echo ""
echo "✅ Tudo validado! Ativando no Paperclip..."
echo ""

# Opção 1: Via Paperclip CLI
if npx paperclipai --version &> /dev/null; then
    echo "📦 Encontrado Paperclip CLI. Ativando via CLI..."
    npx paperclipai routine add --config .claude/config-morning-call.json

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Morning Call ativado com sucesso!"
        echo ""
        echo "📊 Informações da Rotina:"
        echo "  • Horário: Seg-Sex 09h09"
        echo "  • Grupo: 120363407926604570-group"
        echo "  • Conteúdo: content/morning-call/YYYY-MM-DD.md"
        echo "  • Logs: .claude/logs/morning-call.log"
        echo ""
        echo "🔗 Para desativar:"
        echo "  npx paperclipai routine disable morning-call"
        echo ""
        exit 0
    fi
fi

# Opção 2: Via Claude Code
echo "📝 Ativando via Claude Code..."
echo ""
echo "Execute este comando no Claude Code:"
echo ""
echo "  /schedule create \"Morning Call\" \"0 9 * * 1-5\" \"node .claude/scripts/send-morning-call.js\""
echo ""

exit 0
