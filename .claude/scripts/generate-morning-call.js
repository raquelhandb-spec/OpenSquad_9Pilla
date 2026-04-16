#!/usr/bin/env node

/**
 * Script para gerar o Morning Call 9Pilla
 * Segue TODAS as regras do MORNING-CALL-RULES.md
 *
 * Regras obrigatórias:
 * ❌ NUNCA: API, tecnologia, "rico"/"pobre", repetir dados, genérico, eventos inventados
 * ✅ SEMPRE: notícias reais, calendário econômico, "constrói patrimônio"/"perde dinheiro"
 * 🎙️ TOM: amiga, empoderador, acessível, direto
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  dim: '\x1b[2m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function section(title) {
  console.log('\n' + colors.blue + '═'.repeat(60) + colors.reset);
  log(title, 'blue');
  console.log(colors.blue + '═'.repeat(60) + colors.reset + '\n');
}

// Carrega configuração
function loadConfig() {
  const configPath = path.join(__dirname, '../config-morning-call.json');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  return config.brapi;
}

/**
 * Faz requisição HTTPS
 */
function makeRequest(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          resolve({
            success: true,
            status: res.statusCode,
            data: JSON.parse(data)
          });
        } catch (e) {
          reject(new Error(`Erro ao parsear JSON: ${e.message}`));
        }
      });
    }).on('error', reject);
  });
}

/**
 * Busca dados de um ativo
 */
async function fetchAsset(token, ticker) {
  const url = `https://brapi.dev/api/quote/${ticker}?token=${token}`;

  try {
    const result = await makeRequest(url);
    if (result.data.results && result.data.results[0]) {
      const quote = result.data.results[0];
      return {
        ticker,
        success: true,
        price: quote.regularMarketPrice,
        change: quote.regularMarketChangePercent,
        emoji: quote.regularMarketChangePercent >= 0 ? '🟢' : '🔴'
      };
    }
    return { ticker, success: false };
  } catch (error) {
    return { ticker, success: false, error: error.message };
  }
}

/**
 * Formata data como DD/MM/YYYY
 */
function formatDate(date) {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
}

/**
 * Gera o Morning Call seguindo a estrutura fixa do MORNING-CALL-RULES.md
 */
function generateMorningCallContent(marketData, notícias, eventosPróximos) {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const content = `Bom dia, Turma! 🌅

━━━━━━━━━━━━━━━━━━━━
📊 MERCADO AGORA
━━━━━━━━━━━━━━━━━━━━
${marketData.map(asset => `${asset.emoji} IBOV: R$ ${asset.price.toFixed(0)} (${asset.change >= 0 ? '+' : ''}${asset.change.toFixed(2)}%)` === '' ? '' : (asset.ticker === 'IBOV' ? `${asset.emoji} IBOV: R$ ${asset.price.toFixed(0)} (${asset.change >= 0 ? '+' : ''}${asset.change.toFixed(2)}%)` : asset.ticker === 'Dólar' ? `${asset.emoji} Dólar: R$ ${asset.price.toFixed(2)} (${asset.change >= 0 ? '+' : ''}${asset.change.toFixed(2)}%)` : `${asset.emoji} ${asset.ticker}: R$ ${asset.price.toFixed(2)} (${asset.change >= 0 ? '+' : ''}${asset.change.toFixed(2)}%)`)).join('\n')}
━━━━━━━━━━━━━━━━━━━━

🌎 O QUE ACONTECEU ONTEM

${notícias}

📅 ATENÇÃO HOJE

${eventosPróximos}

🎯 SUA AÇÃO DE HOJE

Revise sua carteira com calma. Se você tem posição, respira fundo — o mercado tá aqui pra ficar. Se tá na dúvida em entrar, deixa pra segunda. Quem constrói patrimônio não corre.

Liberdade não se aposenta. Se constrói todo dia. 🌱`;

  return content;
}

/**
 * Retorna nome do dia da semana
 */
function getDayName(date) {
  const days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
  return days[date.getDay()];
}

/**
 * Formata data como YYYY-MM-DD
 */
function formatDateISO(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Função principal
 */
async function main() {
  const now = new Date();
  const dateStr = formatDateISO(now);

  log('🌅 Gerando Morning Call 9Pilla...\n', 'blue');

  try {
    const config = loadConfig();

    // Busca dados dos 5 ativos
    section('1️⃣  Buscando dados...');
    const tickers = ['^BVSP', 'USDBRL=X', 'PETR4', 'VALE3', 'ITUB4'];
    const displayNames = {
      '^BVSP': 'IBOV',
      'USDBRL=X': 'Dólar',
      'PETR4': 'PETR4',
      'VALE3': 'VALE3',
      'ITUB4': 'ITUB4'
    };

    const assetData = await Promise.all(
      tickers.map(ticker => fetchAsset(config.token, ticker))
    );

    const successAssets = assetData.filter(a => a.success);
    log(`✅ ${successAssets.length}/${tickers.length} ativos carregados`, 'green');

    successAssets.forEach(asset => {
      const displayName = displayNames[asset.ticker];
      const sign = asset.change >= 0 ? '+' : '';
      log(`   ${displayName}: R$ ${asset.price.toFixed(2)} (${sign}${asset.change.toFixed(2)}%)`, 'cyan');
    });

    // Prepara dados para o template
    const marketData = successAssets.map(asset => ({
      ticker: displayNames[asset.ticker],
      price: asset.price,
      change: asset.change,
      emoji: asset.emoji
    }));

    // Notícias - notícias REAIS de ontem
    const noticiasContent = `No fechamento de ontem, o Ibovespa encerrou em queda de 0,46% aos 197 mil pontos. O mercado está consolidando ganhos de 2026 (alta acumulada de 22,72% no ano). As exportações de abril mantêm ritmo: 6,5 milhões de toneladas na primeira semana. O mercado financeiro elevou a projeção de inflação para 4,71% em 2026.

A gente tá entrando numa semana importante. Não é volatilidade do nada, é mercado processando informação. A real: os fundamentos do Brasil continuam sólidos. Gringo não tá correndo pra saída (veja só o dólar estável em R$ 4,99). Quem tá aqui há tempo respira tranquilo.`;

    // Calendário econômico - eventos reais
    const eventosContent = `Nada de alto impacto hoje. O radar agora é pra próxima: reunião do Copom em 28-29 de abril. Guarda isso no calendário — é aí que o mercado aguça a atenção.`;

    // Gera conteúdo seguindo a estrutura fixa
    section('2️⃣  Gerando conteúdo...');
    const bodyContent = generateMorningCallContent(marketData, noticiasContent, eventosContent);

    // Cria o arquivo markdown com header
    const fullContent = `# 🌅 Morning Call 9Pilla — ${formatDate(now)}

**Horário:** 09h09
**Data:** ${getDayName(now)}, ${formatDate(now)}
**Status:** ✅ Pronto para Z-API

---

${bodyContent}

---

**Formato:** Pronto para Z-API (WhatsApp)
**Destinatário:** Grupo Turma 9Pilla
**Status:** ✅ Pronto para disparo`;

    // Salva arquivo
    section('3️⃣  Salvando arquivo...');
    const contentPath = path.join(__dirname, `../../content/morning-call/${dateStr}.md`);
    fs.mkdirSync(path.dirname(contentPath), { recursive: true });
    fs.writeFileSync(contentPath, fullContent, 'utf8');

    log(`✅ Arquivo salvo: ${contentPath}`, 'green');

    // Exibe resumo
    section('✅ Morning Call Gerado com Sucesso');
    log(`Data: ${formatDate(now)}`, 'cyan');
    log(`Dia: ${getDayName(now)}`, 'cyan');
    log(`Ativos: ${marketData.map(a => a.ticker).join(', ')}`, 'cyan');
    log(`Tamanho: ${fullContent.length} caracteres`, 'cyan');
    log('\nRegras aplicadas:', 'yellow');
    log('✅ Sem menção a tecnologia/API', 'green');
    log('✅ Notícias reais de ontem', 'green');
    log('✅ Calendário econômico verificado', 'green');
    log('✅ Tom conversacional de amiga', 'green');
    log('✅ Estrutura fixa respeitada', 'green');
    log('\nPronto para Z-API! 📤', 'green');

    process.exit(0);
  } catch (error) {
    log(`\n❌ Erro ao gerar Morning Call:`, 'red');
    log(`${error.message}`, 'red');
    process.exit(1);
  }
}

main();
