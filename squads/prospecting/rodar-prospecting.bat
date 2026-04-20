@echo off
echo.
echo  ╔══════════════════════════════════════╗
echo  ║   SQUAD PROSPECTING — TURMA 9PILLA  ║
echo  ║   CEO: Raquel Santos                 ║
echo  ╚══════════════════════════════════════╝
echo.
echo  Iniciando esteira de prospecting...
echo  Sexta-feira a noite - HORA CERTA!
echo.

cd /d "%~dp0..\.."

echo [1/3] Rodando CEO + Mineradores (YouTube, Reddit, LinkedIn, Instagram)...
gemini --model gemini-2.5-pro-preview-05-06 < squads/prospecting/CEO-prospecting.md

echo.
echo [CONCLUIDO] Verifique: squads/prospecting/data/abordagens_prontas.md
echo.
pause
