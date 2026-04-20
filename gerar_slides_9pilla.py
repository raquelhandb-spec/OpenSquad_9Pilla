# GERADOR DE SLIDES 9PILLA — Python + Pillow
# Uso: python gerar_slides_9pilla.py

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap

# ============================================================
# CONFIGURAÇÕES
# ============================================================

TAMANHO = (1080, 1080)

CORES = {
    'ORANGE':  '#E84A1E',
    'BEIGE':   '#D6C9B0',
    'DARK':    '#1C2E1F',
    'SAND':    '#EDE8DC',
    'WHITE':   '#FFFFFF',
    'BRANCO':  '#FFFFFF',
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

PASTA_FONTES = r"C:\Users\raque\AppData\Local\Microsoft\Windows\Fonts"

def fonte(nome_arquivo, tamanho):
    caminho = os.path.join(PASTA_FONTES, nome_arquivo)
    return ImageFont.truetype(caminho, tamanho)

# ============================================================
# SLIDES POR CARROSSEL
# ============================================================

CARROSSEIS = [
    {
        'id': 'carrossel_01_ibovespa',
        'fundo': 'DARK',
        'texto_cor': 'WHITE',
        'destaque_cor': 'ORANGE',
        'slides': [
            {'num': 1,  'tipo': 'capa',     'titulo': '198 MIL\nPONTOS',           'subtitulo': 'A bolsa bateu recorde.\nVocê sabe o que isso significa?'},
            {'num': 2,  'tipo': 'conteudo', 'titulo': 'O que é o\nIbovespa?',       'subtitulo': 'Índice das maiores empresas\nda bolsa brasileira.\nSe elas vão bem, o índice sobe.'},
            {'num': 3,  'tipo': 'conteudo', 'titulo': 'Por que\nsubiu?',            'subtitulo': 'Investidores estrangeiros\nvoltaram ao Brasil.\nCenário internacional menos turbulento.'},
            {'num': 4,  'tipo': 'conteudo', 'titulo': 'Me afeta sem\nter ações?',   'subtitulo': 'Indiretamente sim.\nEmpresas maiores = mais empregos,\nmais crescimento.'},
            {'num': 5,  'tipo': 'conteudo', 'titulo': 'O que muda\nno meu bolso?',  'subtitulo': 'Praticamente nada,\nse você não investe.\nE esse é o ponto.'},
            {'num': 6,  'tipo': 'conteudo', 'titulo': 'Bolsa sobe\nsem você...',    'subtitulo': 'É como ver\no trem partir.'},
            {'num': 7,  'tipo': 'conteudo', 'titulo': 'Como\ncomeçar?',             'subtitulo': 'Com menos de R$50 você\njá pode comprar frações\nde ação.'},
            {'num': 8,  'tipo': 'conteudo', 'titulo': 'O risco\nexiste.',           'subtitulo': 'Mas ficar fora da bolsa\npor medo também\ntem um custo.'},
            {'num': 9,  'tipo': 'conteudo', 'titulo': 'Próximo\npasso:',            'subtitulo': 'Abrir uma conta\nem uma corretora.\nGratuito. 10 minutos.'},
            {'num': 10, 'tipo': 'cta',      'titulo': 'Salva e\nsegue @9pilla',    'subtitulo': 'Para aprender mais\nsobre investimentos.'},
        ]
    },
    {
        'id': 'carrossel_02_selic',
        'fundo': 'SAND',
        'texto_cor': 'DARK',
        'destaque_cor': 'ORANGE',
        'slides': [
            {'num': 1,  'tipo': 'capa',     'titulo': 'SELIC:\n14,75%',            'subtitulo': 'Isso é bom ou ruim pra você?\nDepende.'},
            {'num': 2,  'tipo': 'conteudo', 'titulo': 'O que é\na Selic?',         'subtitulo': 'É a taxa básica de juros\ndo Brasil. Tudo gira\nem torno dela.'},
            {'num': 3,  'tipo': 'conteudo', 'titulo': 'Quem\ndecide?',             'subtitulo': 'O Copom, do Banco Central,\na cada 45 dias.'},
            {'num': 4,  'tipo': 'conteudo', 'titulo': 'Selic alta\nagora:',        'subtitulo': 'Renda fixa rende mais.\nCrédito fica mais caro.'},
            {'num': 5,  'tipo': 'conteudo', 'titulo': 'Sua\noportunidade:',        'subtitulo': 'Tesouro Selic, CDB,\nLCI, LCA — todos rendem\nmais agora.'},
            {'num': 6,  'tipo': 'conteudo', 'titulo': 'O que NÃO\nfazer:',         'subtitulo': 'Pegar empréstimo\npara consumo.\nOs juros vão te matar.'},
            {'num': 7,  'tipo': 'conteudo', 'titulo': 'O que\nFAZER:',             'subtitulo': 'Pagar dívidas.\nInvestir em renda fixa.\nAgir agora.'},
            {'num': 8,  'tipo': 'conteudo', 'titulo': 'Quando a\nSelic cair:',     'subtitulo': 'Renda fixa rende menos.\nBolsa e imóveis ficam\nmais atraentes.'},
            {'num': 9,  'tipo': 'conteudo', 'titulo': 'Resumo\nprático:',          'subtitulo': 'Agora: renda fixa.\nDepois: diversificar.\nSempre: se educar.'},
            {'num': 10, 'tipo': 'cta',      'titulo': 'Você já\ninveste?',         'subtitulo': 'Comenta aqui:\nvocê já investe\nem renda fixa?'},
        ]
    },
    {
        'id': 'carrossel_03_comportamento',
        'fundo': 'BEIGE',
        'texto_cor': 'DARK',
        'destaque_cor': 'ORANGE',
        'slides': [
            {'num': 1,  'tipo': 'capa',     'titulo': 'Você conhece\nseu dinheiro?',     'subtitulo': '5 sinais de que\ntalvez não.'},
            {'num': 2,  'tipo': 'conteudo', 'titulo': '1.',                              'subtitulo': 'Você não sabe sua\nrenda líquida de cor.\nNão o bruto.\nO que cai na conta.'},
            {'num': 3,  'tipo': 'conteudo', 'titulo': '2.',                              'subtitulo': 'Você descobre que\ngastou demais só\nquando vê o extrato.'},
            {'num': 4,  'tipo': 'conteudo', 'titulo': '3.',                              'subtitulo': 'Você adia organizar\nas finanças faz\nmais de 6 meses.'},
            {'num': 5,  'tipo': 'conteudo', 'titulo': '4.',                              'subtitulo': 'Você tem medo\nde ver o quanto deve.\nO que você não vê,\npiora.'},
            {'num': 6,  'tipo': 'conteudo', 'titulo': '5.',                              'subtitulo': 'Você acha que não\ntem dinheiro sobrando\npra investir.'},
            {'num': 7,  'tipo': 'conteudo', 'titulo': 'A boa\nnotícia:',                'subtitulo': 'Isso não é sobre\ninteligência.\nÉ sobre hábito.'},
            {'num': 8,  'tipo': 'conteudo', 'titulo': 'Primeiro\npasso:',               'subtitulo': 'Anote sua renda\nlíquida hoje.\nSó esse número.'},
            {'num': 9,  'tipo': 'conteudo', 'titulo': 'Segundo\npasso:',                'subtitulo': 'Olhe seu extrato\ndo último mês\nsem julgamento.'},
            {'num': 10, 'tipo': 'cta',      'titulo': 'Se identificou\ncom algum?',     'subtitulo': 'Comenta o número\naqui embaixo.\nSem julgamento.'},
        ]
    },
    {
        'id': 'carrossel_04_dolar',
        'fundo': 'ORANGE',
        'texto_cor': 'WHITE',
        'destaque_cor': 'SAND',
        'slides': [
            {'num': 1,  'tipo': 'capa',     'titulo': 'R$ 5,00',                   'subtitulo': 'O dólar caiu.\nIsso importa pra você?'},
            {'num': 2,  'tipo': 'conteudo', 'titulo': 'O que é\ncâmbio?',          'subtitulo': 'Quanto você paga\nem reais por 1 dólar\namericano.'},
            {'num': 3,  'tipo': 'conteudo', 'titulo': 'Por que\ncaiu?',            'subtitulo': 'Menos incerteza global.\nBrasil mais atrativo\npara investidores.'},
            {'num': 4,  'tipo': 'conteudo', 'titulo': 'O que fica\nmais barato:',  'subtitulo': 'Importados, plataformas\nem dólar, viagens\nao exterior.'},
            {'num': 5,  'tipo': 'conteudo', 'titulo': 'O lado B:',                 'subtitulo': 'Exportações brasileiras\nrendem menos\nao produtor.'},
            {'num': 6,  'tipo': 'conteudo', 'titulo': 'Na prática:',               'subtitulo': 'Amazon, AliExpress,\nNetflix — tudo\nreajusta com câmbio.'},
            {'num': 7,  'tipo': 'conteudo', 'titulo': 'Quer viajar\npra fora?',    'subtitulo': 'Pesquisa agora.\nCâmbio favorável\npode fechar rápido.'},
            {'num': 8,  'tipo': 'conteudo', 'titulo': 'Guardar\ndólar?',           'subtitulo': 'Para proteção de\nlongo prazo, sim.\nNão especulação.'},
            {'num': 9,  'tipo': 'conteudo', 'titulo': 'O câmbio\noscila.',         'subtitulo': 'Sua estratégia\nnão deveria.'},
            {'num': 10, 'tipo': 'cta',      'titulo': 'Salva e\ncompartilha!',     'subtitulo': 'Seu amigo que quer\nviajar precisa\nver isso.'},
        ]
    },
    {
        'id': 'carrossel_05_inflacao',
        'fundo': 'SAND',
        'texto_cor': 'DARK',
        'destaque_cor': 'ORANGE',
        'slides': [
            {'num': 1,  'tipo': 'capa',     'titulo': 'INFLAÇÃO\n2026:',           'subtitulo': 'Acima da meta.\nO que isso significa\npra você?'},
            {'num': 2,  'tipo': 'conteudo', 'titulo': 'O que é\ninflação?',        'subtitulo': 'Aumento geral\ndos preços. Seu dinheiro\ncompra menos.'},
            {'num': 3,  'tipo': 'conteudo', 'titulo': 'O que é\na meta?',          'subtitulo': 'O governo define\num limite de aumento\nanual: 3% (±1,5%).'},
            {'num': 4,  'tipo': 'conteudo', 'titulo': 'O que\naconteceu?',         'subtitulo': 'IPCA de março: 0,88%\nno mês. Projeção 2026:\nacima de 4,5%.'},
            {'num': 5,  'tipo': 'conteudo', 'titulo': 'O que\npuxou?',             'subtitulo': 'Energia elétrica,\nalimentos e serviços.'},
            {'num': 6,  'tipo': 'conteudo', 'titulo': 'Impacto\nno bolso:',        'subtitulo': 'Se você ganhou o mesmo\ne tudo ficou mais caro:\nvocê ficou mais pobre.'},
            {'num': 7,  'tipo': 'conteudo', 'titulo': 'E a\npoupança?',            'subtitulo': 'Rende ~6%/ano.\nCom inflação a 4,5%+,\no ganho some.'},
            {'num': 8,  'tipo': 'conteudo', 'titulo': 'Como se\nproteger?',        'subtitulo': 'Tesouro IPCA+,\nfundos indexados\nà inflação.'},
            {'num': 9,  'tipo': 'conteudo', 'titulo': 'Inflação alta\nnão é o fim.','subtitulo': 'É um sinal\npara agir.'},
            {'num': 10, 'tipo': 'cta',      'titulo': 'Comenta\nINFLAÇÃO',        'subtitulo': 'Que a gente te explica\no Tesouro IPCA+\nem detalhes.'},
        ]
    },
]

# ============================================================
# FUNÇÃO DE GERAÇÃO DE SLIDE
# ============================================================

def gerar_slide(carrossel, slide, caminho_saida):
    W, H = TAMANHO
    img = Image.new('RGB', TAMANHO, hex_to_rgb(CORES[carrossel['fundo']]))
    draw = ImageDraw.Draw(img)

    fundo_cor = carrossel['fundo']
    texto_cor = hex_to_rgb(CORES[carrossel['texto_cor']])
    destaque_cor = hex_to_rgb(CORES[carrossel['destaque_cor']])

    # Linha decorativa lateral esquerda
    draw.rectangle([50, 100, 58, H - 100], fill=destaque_cor)

    # Número do slide — canto superior direito
    try:
        f_num = fonte('DMSans-Regular.ttf', 28)
    except:
        f_num = ImageFont.load_default()

    num_texto = f"{slide['num']}/10"
    draw.text((W - 80, 60), num_texto, font=f_num, fill=texto_cor, anchor='ra')

    # Título principal
    try:
        if slide['tipo'] == 'capa':
            f_titulo = fonte('PlayfairDisplay-ExtraBold.ttf', 110)
        else:
            f_titulo = fonte('PlayfairDisplay-Bold.ttf', 88)
    except:
        f_titulo = ImageFont.load_default()

    titulo_y = 160 if slide['tipo'] == 'capa' else 140
    linhas_titulo = slide['titulo'].split('\n')

    for i, linha in enumerate(linhas_titulo):
        cor_linha = destaque_cor if (slide['tipo'] == 'capa' and i == 0) else texto_cor
        draw.text((100, titulo_y + i * 115 if slide['tipo'] == 'capa' else titulo_y + i * 95),
                  linha, font=f_titulo, fill=cor_linha)

    # Linha separadora
    sep_y = titulo_y + len(linhas_titulo) * (115 if slide['tipo'] == 'capa' else 95) + 30
    draw.rectangle([100, sep_y, 400, sep_y + 3], fill=destaque_cor)

    # Subtítulo
    try:
        f_sub = fonte('DMSans-Regular.ttf', 46)
    except:
        f_sub = ImageFont.load_default()

    sub_y = sep_y + 40
    linhas_sub = slide['subtitulo'].split('\n')
    for i, linha in enumerate(linhas_sub):
        draw.text((100, sub_y + i * 58), linha, font=f_sub, fill=texto_cor)

    # Logo 9Pilla — canto inferior direito
    try:
        f_logo_num = fonte('PlayfairDisplay-Bold.ttf', 42)
        f_logo_txt = fonte('DMSans-Bold.ttf', 42)
    except:
        f_logo_num = ImageFont.load_default()
        f_logo_txt = f_logo_num

    logo_y = H - 80
    draw.text((W - 160, logo_y), "9", font=f_logo_num, fill=destaque_cor, anchor='la')
    draw.text((W - 132, logo_y), "Pilla", font=f_logo_txt, fill=texto_cor, anchor='la')

    # Salva
    img.save(caminho_saida, 'PNG', quality=95)

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    pasta_base = os.path.join(os.getcwd(), 'content', 'slides_pillow')
    os.makedirs(pasta_base, exist_ok=True)

    print("🎨 GERADOR DE SLIDES 9PILLA — Python + Pillow")
    print("=" * 50)

    total = 0
    erros = 0

    for carrossel in CARROSSEIS:
        print(f"\n📊 {carrossel['id']}")
        pasta_carrossel = os.path.join(pasta_base, carrossel['id'])
        os.makedirs(pasta_carrossel, exist_ok=True)

        for slide in carrossel['slides']:
            nome = f"slide_{str(slide['num']).zfill(2)}.png"
            caminho = os.path.join(pasta_carrossel, nome)

            try:
                gerar_slide(carrossel, slide, caminho)
                print(f"  Slide {slide['num']:02d}/10 ✅")
                total += 1
            except Exception as e:
                print(f"  Slide {slide['num']:02d}/10 ❌ {e}")
                erros += 1

    print("\n" + "=" * 50)
    print(f"✅ Gerados: {total} slides")
    print(f"❌ Erros: {erros}")
    print(f"📁 Pasta: {pasta_base}")

if __name__ == '__main__':
    main()
