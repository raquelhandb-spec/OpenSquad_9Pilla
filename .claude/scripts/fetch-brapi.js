#!/usr/bin/env node

/**
 * Script para buscar dados da brapi.dev
 * Testa conexão e valida os dados de PETR4, VALE3, ITUB4, IBOVESPA e Dólar
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

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
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve({
              success: true,
              status: res.statusCode,
              data: JSON.parse(data)
            });
          } catch (e) {
            reject(new Error(`Erro ao parsear JSON: ${e.message}`));
          }
        } else {
          reject(new Error(`Status ${res.statusCode}: ${data}`));
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
    return {
      ticker,
      success: true,
      data: result.data
    };
  } catch (error) {
    return {
      ticker,
      success: false,
      error: error.message
    };
  }
}

/**
 * Formata número como moeda
 */
function formatCurrency(value) {
  return `R$ ${Number(value).toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;
}

/**
 * Formata nome do ticker para exibição
 */
function getTickerDisplayName(ticker) {
  const names = {
    '^BVSP': 'IBOVESPA',
    'USDBRL=X': 'Dólar (USD/BRL)',
    'PETR4': 'Petrobras',
    'VALE3': 'Vale',
    'ITUB4': 'Itaú'
  };
  return names[ticker] || ticker;
}

/**
 * Função principal
 */
async function main() {
  log('📊 Teste de Conexão - brapi.dev\n', 'blue');

  try {
    const config = loadConfig();
    log(`Token: ${config.token.substring(0, 10)}...`, 'dim');
    log(`Base URL: ${config.baseUrl}\n`, 'dim');

    // Tickers a buscar: IBOVESPA, Dólar, PETR4, VALE3, ITUB4
    const tickers = ['^BVSP', 'USDBRL=X', 'PETR4', 'VALE3', 'ITUB4'];

    section(`Buscando dados de ${tickers.length} ativos...`);

    const results = await Promise.all(
      tickers.map(ticker => fetchAsset(config.token, ticker))
    );

    let successCount = 0;
    let failureCount = 0;
    const failedTickers = [];

    results.forEach((result) => {
      console.log();

      if (result.success) {
        log(`✅ ${getTickerDisplayName(result.ticker)} (${result.ticker})`, 'green');
        const quote = result.data.results?.[0];

        if (quote) {
          log(`   Preço: ${formatCurrency(quote.regularMarketPrice)}`, 'cyan');
          const change = Number(quote.regularMarketChangePercent);
          log(`   Variação: ${change.toFixed(2)}%`,
            change >= 0 ? 'green' : 'red');
          log(`   Volume: ${(quote.regularMarketVolume / 1000000).toFixed(1)}M`, 'dim');
          successCount++;
        } else {
          log(`   ⚠️  Dados não encontrados na resposta`, 'yellow');
          failureCount++;
          failedTickers.push(result.ticker);
        }
      } else {
        log(`❌ ${getTickerDisplayName(result.ticker)} (${result.ticker})`, 'red');
        log(`   Erro: ${result.error}`, 'red');
        failureCount++;
        failedTickers.push(result.ticker);
      }
    });

    section('📊 Resumo');
    log(`Sucesso: ${successCount}/${tickers.length}`, successCount === tickers.length ? 'green' : 'yellow');
    log(`Falhas: ${failureCount}/${tickers.length}`, failureCount === 0 ? 'green' : 'red');

    if (successCount === tickers.length) {
      log('\n✅ Todas as 5 conexões foram bem-sucedidas!', 'green');
      log('A chave da brapi.dev está funcionando corretamente para todos os ativos.', 'green');
      section('📈 Ativos Disponíveis');
      results.forEach(r => {
        if (r.success) {
          const quote = r.data.results?.[0];
          if (quote) {
            log(`${getTickerDisplayName(r.ticker)}: ${formatCurrency(quote.regularMarketPrice)} (${Number(quote.regularMarketChangePercent).toFixed(2)}%)`, 'green');
          }
        }
      });
      process.exit(0);
    } else if (successCount > 0) {
      log('\n✅ A chave da brapi.dev está funcionando!', 'green');
      log(`${successCount}/${tickers.length} ativos obtidos com sucesso.`, 'green');
      if (failedTickers.length > 0) {
        log(`\n⚠️  Nota: Tickers ${failedTickers.join(', ')} não foram encontrados.`, 'yellow');
      }
      section('📈 Ativos Disponíveis');
      results.forEach(r => {
        if (r.success) {
          const quote = r.data.results?.[0];
          if (quote) {
            log(`${getTickerDisplayName(r.ticker)}: ${formatCurrency(quote.regularMarketPrice)} (${Number(quote.regularMarketChangePercent).toFixed(2)}%)`, 'green');
          }
        }
      });
      process.exit(0);
    } else {
      log('\n❌ Nenhuma conexão foi bem-sucedida.', 'red');
      process.exit(1);
    }

  } catch (error) {
    log(`\n❌ Erro ao carregar configuração ou executar teste:`, 'red');
    log(`${error.message}`, 'red');
    process.exit(1);
  }
}

main();
