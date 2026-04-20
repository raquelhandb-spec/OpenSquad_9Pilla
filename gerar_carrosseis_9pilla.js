// GERADOR DE CARROSSÉIS 9PILLA — Imagen 4 + Gemini 2.5 Flash
// Uso: node gerar_carrosseis_9pilla.js
// Requer: GEMINI_API_KEY no ambiente

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_KEY = process.env.GEMINI_API_KEY;

if (!API_KEY) {
  console.error('ERRO: GEMINI_API_KEY não encontrada. Rode: $env:GEMINI_API_KEY="sua_key"');
  process.exit(1);
}

// Paleta oficial 9Pilla
const PALETA = {
  ORANGE: '#E84A1E',
  BEIGE: '#D6C9B0',
  DARK: '#1C2E1F',
  SAND: '#EDE8DC'
};

// Slides da semana (gerados pelo pacote aprovado)
const CARROSSEIS = [
  {
    id: 'carrossel_01_ibovespa',
    tema: 'Ibovespa bateu recorde. O que isso muda pra você?',
    estilo: 'Editorial Imperfeito com textura. Fundo escuro #1C2E1F, números grandes em laranja #E84A1E, granulado sutil',
    slides: [
      { num: 1, tipo: 'capa', texto: '198 MIL PONTOS. A bolsa bateu recorde. Você sabe o que isso significa?' },
      { num: 2, tipo: 'conteudo', texto: 'O que é o Ibovespa? Índice das maiores empresas da bolsa brasileira.' },
      { num: 3, tipo: 'conteudo', texto: 'Por que subiu? Investidores estrangeiros voltaram ao Brasil.' },
      { num: 4, tipo: 'conteudo', texto: 'Isso me afeta se eu não tenho ações? Indiretamente sim.' },
      { num: 5, tipo: 'conteudo', texto: 'O que muda no meu bolso AGORA? Praticamente nada, se você não investe.' },
      { num: 6, tipo: 'conteudo', texto: 'Quando a bolsa sobe e você não está nela... é como ver o trem partir.' },
      { num: 7, tipo: 'conteudo', texto: 'Como começar na bolsa? Com menos de R$50 você já pode comprar frações.' },
      { num: 8, tipo: 'conteudo', texto: 'O risco existe. Mas ficar fora da bolsa por medo também tem um custo.' },
      { num: 9, tipo: 'conteudo', texto: 'Próximo passo: abrir uma conta em uma corretora. Gratuito. 10 minutos.' },
      { num: 10, tipo: 'cta', texto: 'Salva esse carrossel e segue @9pilla para aprender mais.' }
    ]
  },
  {
    id: 'carrossel_02_selic',
    tema: 'O que é a Selic e por que você deveria se importar',
    estilo: 'Clean Editorial. Fundo areia #EDE8DC, traços laranja #E84A1E, tipografia bold',
    slides: [
      { num: 1, tipo: 'capa', texto: 'SELIC: 14,75%. Isso é bom ou ruim pra você? Depende.' },
      { num: 2, tipo: 'conteudo', texto: 'O que é a Selic? É a taxa básica de juros do Brasil.' },
      { num: 3, tipo: 'conteudo', texto: 'Quem decide? O Copom, do Banco Central, a cada 45 dias.' },
      { num: 4, tipo: 'conteudo', texto: 'Selic alta: renda fixa rende mais. Crédito fica mais caro.' },
      { num: 5, tipo: 'conteudo', texto: 'Tesouro Selic, CDB, LCI, LCA: todos rendem mais agora.' },
      { num: 6, tipo: 'conteudo', texto: 'O que NÃO fazer: pegar empréstimo pra consumo. Os juros vão te matar.' },
      { num: 7, tipo: 'conteudo', texto: 'O que FAZER: pagar dívidas. Investir em renda fixa. Agir agora.' },
      { num: 8, tipo: 'conteudo', texto: 'Quando a Selic cair: renda fixa rende menos. Bolsa fica atraente.' },
      { num: 9, tipo: 'conteudo', texto: 'Resumo: agora renda fixa. Depois diversificar. Sempre se educar.' },
      { num: 10, tipo: 'cta', texto: 'Comenta aqui: você já investe em renda fixa?' }
    ]
  },
  {
    id: 'carrossel_03_comportamento',
    tema: '5 sinais de que você não conhece seu próprio dinheiro',
    estilo: 'Confessional Zine. Fundo bege #D6C9B0 com imperfeições, mix de manuscrito e digital',
    slides: [
      { num: 1, tipo: 'capa', texto: 'Você conhece seu dinheiro? 5 sinais de que talvez não.' },
      { num: 2, tipo: 'conteudo', texto: '1. Você não sabe sua renda líquida de cor. Não o bruto. O que cai na conta.' },
      { num: 3, tipo: 'conteudo', texto: '2. Você descobre que gastou demais só quando vê o extrato.' },
      { num: 4, tipo: 'conteudo', texto: '3. Você adia organizar as finanças faz mais de 6 meses.' },
      { num: 5, tipo: 'conteudo', texto: '4. Você tem medo de ver o quanto deve. O que você não vê, piora.' },
      { num: 6, tipo: 'conteudo', texto: '5. Você acha que não tem dinheiro sobrando pra investir.' },
      { num: 7, tipo: 'conteudo', texto: 'A boa notícia: isso não é sobre inteligência. É sobre hábito.' },
      { num: 8, tipo: 'conteudo', texto: 'Primeiro passo: anote sua renda líquida hoje. Só esse número.' },
      { num: 9, tipo: 'conteudo', texto: 'Segundo passo: olhe seu extrato do último mês sem julgamento.' },
      { num: 10, tipo: 'cta', texto: 'Você se identificou com algum? Comenta o número aqui.' }
    ]
  },
  {
    id: 'carrossel_04_dolar',
    tema: 'Dólar a R$5 — o que muda na sua vida?',
    estilo: 'Moderno Tátil. Gradiente laranja para areia, tipografia forte',
    slides: [
      { num: 1, tipo: 'capa', texto: 'R$ 5,00. O dólar caiu. Isso importa pra você?' },
      { num: 2, tipo: 'conteudo', texto: 'O que é a taxa de câmbio? Quanto você paga em reais por 1 dólar.' },
      { num: 3, tipo: 'conteudo', texto: 'Por que o dólar caiu? Menos incerteza global, Brasil mais atrativo.' },
      { num: 4, tipo: 'conteudo', texto: 'O que fica mais barato: importados, plataformas em dólar, viagens.' },
      { num: 5, tipo: 'conteudo', texto: 'O lado B: exportações brasileiras rendem menos ao produtor.' },
      { num: 6, tipo: 'conteudo', texto: 'Na prática: Amazon, AliExpress, Netflix — tudo reajusta com câmbio.' },
      { num: 7, tipo: 'conteudo', texto: 'Quer viajar pra fora? Pesquisa agora. Câmbio favorável pode fechar.' },
      { num: 8, tipo: 'conteudo', texto: 'Guardar dólar? Para proteção de longo prazo, sim. Não especulação.' },
      { num: 9, tipo: 'conteudo', texto: 'O câmbio oscila. Sua estratégia não deveria.' },
      { num: 10, tipo: 'cta', texto: 'Salva e compartilha. Teu amigo que quer viajar precisa ver isso.' }
    ]
  },
  {
    id: 'carrossel_05_inflacao',
    tema: 'A inflação tá acima da meta. Isso é grave?',
    estilo: 'Direto e visual. Fundo areia #EDE8DC, dados em destaque laranja #E84A1E',
    slides: [
      { num: 1, tipo: 'capa', texto: 'INFLAÇÃO 2026: acima da meta. O que isso significa pra você?' },
      { num: 2, tipo: 'conteudo', texto: 'O que é inflação? Aumento geral dos preços. Seu dinheiro compra menos.' },
      { num: 3, tipo: 'conteudo', texto: 'O que é a meta? O governo define um limite de aumento anual: 3% (±1,5%).' },
      { num: 4, tipo: 'conteudo', texto: 'IPCA de março: 0,88% no mês. Projeção 2026: acima de 4,5%.' },
      { num: 5, tipo: 'conteudo', texto: 'O que puxou os preços? Energia elétrica, alimentos, serviços.' },
      { num: 6, tipo: 'conteudo', texto: 'Se você ganhou o mesmo e tudo ficou mais caro: você ficou mais pobre.' },
      { num: 7, tipo: 'conteudo', texto: 'E a poupança? Rende ~6%/ano. Com inflação a 4,5%+, o ganho some.' },
      { num: 8, tipo: 'conteudo', texto: 'Como se proteger? Tesouro IPCA+, fundos indexados à inflação.' },
      { num: 9, tipo: 'conteudo', texto: 'Inflação alta não é o fim do mundo. É um sinal para agir.' },
      { num: 10, tipo: 'cta', texto: 'Comenta INFLAÇÃO aqui que a gente te explica o Tesouro IPCA+.' }
    ]
  }
];

// Função para gerar prompt de imagem para cada slide
function gerarPromptImagem(carrossel, slide) {
  const cores = `cores oficiais da marca: laranja vibrante #E84A1E como cor principal, bege #D6C9B0, verde escuro #1C2E1F, areia #EDE8DC`;
  const tipografia = `tipografia Playfair Display bold para títulos, DM Sans para corpo`;
  const estilo = carrossel.estilo;

  let promptBase = `
Crie um slide de carrossel para Instagram (formato 1080x1080px) para uma empresa brasileira de educação financeira chamada 9Pilla.

ESTILO VISUAL: ${estilo}
CORES: ${cores}
TIPOGRAFIA: ${tipografia}
TEXTO DO SLIDE: "${slide.texto}"

REGRAS OBRIGATÓRIAS:
- NÃO usar verde e amarelo juntos (conotação política brasileira)
- Visual moderno, editorial, cool — não é banco, não é consultoria formal
- Textura sutil de papel ou granulado
- Logo 9Pilla pequeno no canto inferior direito
- Texto legível, grande, com hierarquia visual clara
- Slide ${slide.num} de 10 ${slide.tipo === 'capa' ? '(CAPA — impacto máximo)' : slide.tipo === 'cta' ? '(CTA — call to action)' : '(conteúdo)'}
`;

  return promptBase.trim();
}

// Função para chamar Imagen 4
function gerarImagem(prompt, outputPath) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      instances: [{ prompt: prompt }],
      parameters: {
        sampleCount: 1,
        aspectRatio: '1:1',
        safetyFilterLevel: 'block_few'
      }
    });

    const options = {
      hostname: 'generativelanguage.googleapis.com',
      path: `/v1beta/models/imagen-4.0-generate-001:predict?key=${API_KEY}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.predictions && json.predictions[0] && json.predictions[0].bytesBase64Encoded) {
            const imageBuffer = Buffer.from(json.predictions[0].bytesBase64Encoded, 'base64');
            fs.writeFileSync(outputPath, imageBuffer);
            resolve(outputPath);
          } else {
            reject(new Error(`Resposta inesperada: ${data.substring(0, 200)}`));
          }
        } catch (e) {
          reject(new Error(`Erro ao parsear resposta: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// Função principal
async function gerarTodosCarrosseis() {
  const outputDir = path.join(process.cwd(), 'content', 'carrosseis');

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log('🎨 GERADOR DE CARROSSÉIS 9PILLA');
  console.log('================================');
  console.log(`📁 Salvando em: ${outputDir}`);
  console.log('');

  let totalGerados = 0;
  let totalErros = 0;

  for (const carrossel of CARROSSEIS) {
    console.log(`\n📊 ${carrossel.tema}`);
    const carrosselDir = path.join(outputDir, carrossel.id);

    if (!fs.existsSync(carrosselDir)) {
      fs.mkdirSync(carrosselDir, { recursive: true });
    }

    for (const slide of carrossel.slides) {
      const outputPath = path.join(carrosselDir, `slide_${String(slide.num).padStart(2, '0')}.png`);
      const prompt = gerarPromptImagem(carrossel, slide);

      process.stdout.write(`  Slide ${slide.num}/10... `);

      try {
        await gerarImagem(prompt, outputPath);
        console.log(`✅ salvo`);
        totalGerados++;

        // Pausa entre requests para não exceder rate limit
        await new Promise(r => setTimeout(r, 2000));

      } catch (err) {
        console.log(`❌ erro: ${err.message.substring(0, 80)}`);
        totalErros++;

        // Salva prompt em txt para geração manual se necessário
        fs.writeFileSync(
          outputPath.replace('.png', '_prompt.txt'),
          prompt
        );
      }
    }
  }

  console.log('\n================================');
  console.log(`✅ Gerados: ${totalGerados} slides`);
  console.log(`❌ Erros: ${totalErros} slides`);
  console.log(`📁 Pasta: ${outputDir}`);
  console.log('\nPróximo passo: leve os slides para o HeyGen para os Reels!');
}

gerarTodosCarrosseis().catch(console.error);
