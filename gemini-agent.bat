@echo off
cd /d C:\Users\raque\OpenSquad_9Pilla
:: Carregar variaveis do .env
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    set %%a=%%b
)
:: Remover aspas para evitar erro no comando
set GEMINI_API_KEY=%GEMINI_API_KEY:"=%
:: Rodar gemini lendo explicitamente da entrada padrao (stdin)
gemini --prompt - --approval-mode yolo
