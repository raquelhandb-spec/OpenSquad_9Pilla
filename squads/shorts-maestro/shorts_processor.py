#!/usr/bin/env python3
"""
📹 SHORTS PROCESSOR — Converte Morning Call em 3 scripts de vídeo curto

Input: MC_20260613.txt (Morning Call completo)
Output: 3 scripts de 60-90s (bloco1, bloco2, bloco3)

Cada script vai para:
- ElevenLabs (gera áudio com voz Raquel)
- HeyGen (gera vídeo com avatar)
- FFmpeg (adiciona legendas + Canva design)
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'shorts')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_section(text, section_name):
    """Extrai uma seção do Morning Call por nome"""
    pattern = rf'\[{section_name}\](.*?)(?=\n\[|$)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def process_morning_call(mc_file):
    """Processa 1 Morning Call completo e extrai os 3 blocos principais"""

    print("=" * 70)
    print("📹 SHORTS PROCESSOR — Processando Morning Call")
    print("=" * 70)

    # Ler arquivo
    if not os.path.exists(mc_file):
        print(f"❌ Arquivo não encontrado: {mc_file}")
        return False

    with open(mc_file, 'r', encoding='utf-8') as f:
        mc_text = f.read()

    # Extrair seções
    print("\n[1/3] 🔍 Extraindo BLOCOS principais...")

    bloco1 = extract_section(mc_text, 'BLOCO 1|BLOCO1|bloco 1|bloco1|🔥.*?1')
    bloco2 = extract_section(mc_text, 'BLOCO 2|BLOCO2|bloco 2|bloco2|🔥.*?2')
    bloco3 = extract_section(mc_text, 'BLOCO 3|BLOCO3|bloco 3|bloco3|🔥.*?3')

    # Se não encontrar com números, pegar os primeiros 3 parágrafos significativos
    if not (bloco1 and bloco2 and bloco3):
        print("   ⚠️ Blocos estruturados não encontrados, extraindo por padrão...")
        paragraphs = [p.strip() for p in mc_text.split('\n\n') if len(p.strip()) > 200]
        if len(paragraphs) >= 3:
            bloco1 = paragraphs[1]  # Skip abertura, pega análise 1
            bloco2 = paragraphs[2]  # Análise 2
            bloco3 = paragraphs[3] if len(paragraphs) > 3 else paragraphs[2]  # Análise 3

    blocos = {
        'bloco1': bloco1[:500],  # Limita a 500 chars (60-90s de fala)
        'bloco2': bloco2[:500],
        'bloco3': bloco3[:500]
    }

    # Gerar scripts para vídeo
    print("[2/3] 📝 Gerando scripts para vídeo (60-90s cada)...")

    mc_date = os.path.basename(mc_file).replace('MC_', '').replace('.txt', '').replace('.md', '')
    scripts = {}

    for i, (key, content) in enumerate(blocos.items(), 1):
        # Limpar conteúdo
        content = re.sub(r'\[.*?\]', '', content)  # Remove tags
        content = re.sub(r'#{1,6}\s', '', content)  # Remove headers markdown
        content = re.sub(r'\*\*|\*|_', '', content)  # Remove bold/italic
        content = re.sub(r'→|→→|►|▼|◆', '', content)  # Remove setas

        # Estruturar para vídeo
        script = f"""[VÍDEO {i}/3] {mc_date}

Olá! Aqui é a Raquel! ☕

{content.strip()}

Fica o alerta: sempre pesquise antes de operar.

Raquel | 9Pilla
Dinheiro não é destino. É a jornada para a liberdade. 💛

⚠️ Educacional. CVM Res. 20/2021.
"""
        scripts[key] = script
        print(f"   ✅ BLOCO {i}: {len(content)} caracteres ({len(content.split())//150 + 1} min)")

    # Salvar scripts
    print("\n[3/3] 💾 Salvando scripts para vídeo...")

    shorts_dir = os.path.join(OUTPUT_DIR, f'MC_{mc_date}')
    os.makedirs(shorts_dir, exist_ok=True)

    metadata = {
        'mc_date': mc_date,
        'created_at': datetime.now().isoformat(),
        'shorts': {}
    }

    for key, script in scripts.items():
        file_path = os.path.join(shorts_dir, f'{key}.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(script)

        metadata['shorts'][key] = {
            'file': file_path,
            'chars': len(script),
            'words': len(script.split()),
            'estimated_duration_sec': len(script.split()) // 2.5  # ~2.5 palavras por segundo
        }

        print(f"   ✅ {key}.txt salvo")

    # Salvar metadados
    metadata_file = os.path.join(shorts_dir, 'metadata.json')
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print(f"✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"   Pasta: {shorts_dir}")
    print(f"   Scripts prontos para ElevenLabs → HeyGen → Canva")
    print("=" * 70)

    return {
        'shorts_dir': shorts_dir,
        'metadata': metadata,
        'scripts': scripts
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        mc_file = sys.argv[1]
    else:
        # Procurar o Morning Call mais recente
        output_dir = os.path.join(BASE_DIR, 'output')
        mc_files = [f for f in os.listdir(output_dir) if f.startswith('MC_') and f.endswith(('.txt', '.md'))]

        if not mc_files:
            print("❌ Nenhum Morning Call encontrado em output/")
            sys.exit(1)

        mc_file = os.path.join(output_dir, sorted(mc_files)[-1])
        print(f"📝 Processando: {os.path.basename(mc_file)}\n")

    result = process_morning_call(mc_file)

    if result:
        print("\n🚀 PRÓXIMO PASSO:")
        print("   python video_generator.py (gera vídeos com HeyGen)")
