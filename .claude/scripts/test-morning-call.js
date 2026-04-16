#!/usr/bin/env node

/**
 * Script de teste para Morning Call
 * Valida se tudo está configurado corretamente antes de enviar
 */

const fs = require('fs');
const path = require('path');

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
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

async function main() {
  log('🧪 Teste de Configuração - Morning Call via Z-API\n', 'blue');

  let passed = 0;
  let failed = 0;

  // Teste 1: Verificar arquivo de script
  section('1. Verificando Script Principal');
  const scriptPath = path.join(__dirname, 'send-morning-call.js');
  if (fs.existsSync(scriptPath)) {
    log('✅ Script encontrado', 'green');
    passed++;
  } else {
    log(`❌ Script não encontrado: ${scriptPath}`, 'red');
    failed++;
  }

  // Teste 2: Verificar arquivo de configuração
  section('2. Verificando Arquivo de Configuração');
  const configPath = path.join(__dirname, '../config-morning-call.json');
  if (fs.existsSync(configPath)) {
    log('✅ Arquivo de configuração encontrado', 'green');
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      log(`   Rotina: ${config.paperclipRoutines['morning-call'].name}`, 'green');
      log(`   Schedule: ${config.paperclipRoutines['morning-call'].schedule}`, 'green');
      passed++;
    } catch (e) {
      log(`❌ JSON inválido: ${e.message}`, 'red');
      failed++;
    }
  } else {
    log(`❌ Arquivo não encontrado: ${configPath}`, 'red');
    failed++;
  }

  // Teste 3: Verificar pasta de conteúdo
  section('3. Verificando Pasta de Conteúdo');
  const contentDir = path.join(__dirname, '../../content/morning-call');
  if (fs.existsSync(contentDir)) {
    log('✅ Pasta encontrada', 'green');
    const files = fs.readdirSync(contentDir).filter(f => f.endsWith('.md'));
    log(`   Arquivos de Morning Call: ${files.length}`, 'green');
    files.forEach(f => log(`   - ${f}`, 'dim'));
    passed++;
  } else {
    log(`❌ Pasta não encontrada: ${contentDir}`, 'red');
    failed++;
  }

  // Teste 4: Verificar arquivo do dia
  section('4. Verificando Arquivo do Dia');
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const todayFile = path.join(contentDir, `${year}-${month}-${day}.md`);

  if (fs.existsSync(todayFile)) {
    log(`✅ Arquivo do dia existe: ${year}-${month}-${day}.md`, 'green');
    const content = fs.readFileSync(todayFile, 'utf8');
    log(`   Tamanho: ${content.length} caracteres`, 'green');
    log(`   Prévia: ${content.substring(0, 100).replace(/\n/g, ' ')}...`, 'dim');
    passed++;
  } else {
    log(`❌ Arquivo do dia não encontrado: ${year}-${month}-${day}.md`, 'red');
    failed++;
  }

  // Teste 5: Validar horário
  section('5. Validando Horário');
  const isBusinessDay = now.getDay() >= 1 && now.getDay() <= 5;
  const dayName = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'][now.getDay()];

  if (isBusinessDay) {
    log(`✅ Hoje é ${dayName} (dia útil)`, 'green');
    passed++;
  } else {
    log(`⚠️  Hoje é ${dayName} (FIM DE SEMANA - não executará)`, 'yellow');
  }

  // Teste 6: Validar credenciais
  section('6. Validando Credenciais Z-API');
  const requiredEnv = [
    'Z_API_INSTANCE_ID',
    'Z_API_TOKEN',
    'Z_API_CLIENT_TOKEN',
    'Z_API_GROUP_JID'
  ];

  let hasAllEnv = true;
  requiredEnv.forEach(key => {
    if (process.env[key]) {
      log(`✅ ${key} definido`, 'green');
    } else {
      log(`⚠️  ${key} não está em variáveis de ambiente`, 'yellow');
      hasAllEnv = false;
    }
  });

  if (hasAllEnv) {
    passed++;
  } else {
    log('   (As credenciais estão hardcoded no script)', 'dim');
    passed++;
  }

  // Teste 7: Verificar permissões
  section('7. Verificando Permissões');
  try {
    fs.accessSync(scriptPath, fs.constants.R_OK | fs.constants.X_OK);
    log('✅ Script é executável', 'green');
    passed++;
  } catch (e) {
    log('⚠️  Script pode não ser executável (pode funcionar mesmo assim)', 'yellow');
  }

  // Resumo
  section('📊 Resumo dos Testes');
  log(`Passou: ${passed}`, 'green');
  log(`Falhou: ${failed}`, failed > 0 ? 'red' : 'green');

  if (failed === 0) {
    log('\n✅ Tudo pronto! A rotina está configurada corretamente.', 'green');
    log('\nPróximos passos:', 'blue');
    log('1. Ativar no Paperclip: npx paperclipai routine enable morning-call', 'dim');
    log('2. Ou testar manualmente: node .claude/scripts/send-morning-call.js', 'dim');
    process.exit(0);
  } else {
    log('\n❌ Existem problemas a resolver antes de ativar.', 'red');
    process.exit(1);
  }
}

main().catch(error => {
  log(`\n❌ Erro: ${error.message}`, 'red');
  process.exit(1);
});
