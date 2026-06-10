#!/bin/bash

# 🚀 Setup Rápido 9Pilla Shorts-Maestro
# Execute: bash setup-quick.sh

set -e  # Parar se erro

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         9PILLA SHORTS-MAESTRO — SETUP RÁPIDO               ║"
echo "║                  Aperte Enter para começar                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
read -p ""

# Passo 1: Python venv
echo ""
echo "📦 [1/4] Criando ambiente Python..."
python3 -m venv venv
source venv/bin/activate

echo "📦 [2/4] Instalando dependências..."
pip install -q -r requirements.txt

echo ""
echo "✅ Ambiente Python pronto!"

# Passo 2: Copiar .env
echo ""
echo "⚙️  [3/4] Configurando arquivo .env..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env criado (EDITE com seu Telegram token!)"
else
    echo "ℹ️  .env já existe (usando existente)"
fi

# Passo 3: Validar
echo ""
echo "🔍 [4/4] Validando setup..."

# Verificar Python
python_check=$(python3 --version 2>&1)
echo "✅ Python: $python_check"

# Verificar dependências
if python3 -c "import requests, dotenv" 2>/dev/null; then
    echo "✅ Dependências instaladas"
else
    echo "⚠️  Erro ao instalar dependências"
    exit 1
fi

# Verificar Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama rodando (http://localhost:11434)"
else
    echo "⚠️  Ollama NÃO está rodando!"
    echo "   Abra novo terminal e execute: ollama serve"
    echo ""
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETO! ✅                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 PRÓXIMAS ETAPAS:"
echo ""
echo "1. Edite o arquivo .env:"
echo "   nano .env"
echo ""
echo "2. Procure por TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID"
echo "   (ou use os defaults já preenchidos)"
echo ""
echo "3. Se Ollama NÃO estava rodando, abra novo terminal e execute:"
echo "   ollama serve"
echo ""
echo "4. Depois execute:"
echo "   python orchestrator.py --validate"
echo ""
echo "5. Se tudo passar, rode:"
echo "   python orchestrator.py --cycle"
echo ""
echo "🎉 Seu primeiro short será publicado!"
echo ""
