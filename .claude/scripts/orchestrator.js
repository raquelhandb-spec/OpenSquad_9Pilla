#!/usr/bin/env node

/**
 * Caio Content Orchestrator
 *
 * Lê 9pilla-orchestrator.yml e roteia requisições para agentes corretos
 * Valida constitution rules antes de publicar
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const CONFIG_PATH = path.join(__dirname, '../config/9pilla-orchestrator.yml');
const CONTENT_DIR = path.join(__dirname, '../../content');

class Orchestrator {
  constructor() {
    this.config = this.loadConfig();
    this.task = process.argv[2];
    this.args = process.argv.slice(3);
  }

  loadConfig() {
    try {
      const configFile = fs.readFileSync(CONFIG_PATH, 'utf8');
      return yaml.load(configFile);
    } catch (err) {
      console.error('❌ Erro ao ler config:', err.message);
      process.exit(1);
    }
  }

  getRoutingRules(trigger) {
    const rules = this.config.agents[0].routing_rules;
    const rule = rules.find(r => r.trigger.toLowerCase() === trigger.toLowerCase());

    if (!rule) {
      console.error(`🚫 Trigger não encontrado: ${trigger}`);
      process.exit(1);
    }

    return rule;
  }

  validateConstitution(content) {
    const constitution = this.config.constitution;
    const issues = [];

    // Check banned words
    for (const word of constitution.banned_words) {
      if (content.toLowerCase().includes(word.toLowerCase())) {
        issues.push({
          type: 'BANNED_WORD',
          word: word,
          message: `Palavra banida detectada: "${word}"`
        });
      }
    }

    // Check for dash in running text (only allow in tables/lists)
    const dashPattern = /[—–]/g;
    const lines = content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (dashPattern.test(line) && !line.includes('|')) {
        issues.push({
          type: 'DASH_IN_TEXT',
          line: i + 1,
          message: `Travessão encontrado em texto corrido (linha ${i + 1})`
        });
      }
    }

    // Check for CVM disclaimer (if content is about markets)
    if (content.toLowerCase().includes('ibov') ||
        content.toLowerCase().includes('petr4') ||
        content.toLowerCase().includes('market')) {
      if (!content.includes('CVM Resolução 20/2021')) {
        issues.push({
          type: 'MISSING_DISCLAIMER',
          message: 'Disclaimer CVM não encontrado em conteúdo de mercado'
        });
      }
    }

    return issues;
  }

  async executeAgent(agentId, input) {
    console.log(`⏳ Invocando ${agentId}...`);

    // Mock: em produção, isto invocaria via Claude API ou MCP
    // Por enquanto, retorna estrutura esperada

    const agentMap = {
      'amorim-analista': () => ({
        success: true,
        agent: 'amorim-analista',
        output: '📊 Análise de mercado estruturada (mock)',
        termometro: '| PETR4 | 38,70 | +0,80% | ▲ |'
      }),
      'redacao-9pilla': () => ({
        success: true,
        agent: 'redacao-9pilla',
        output: '📝 Morning Call redação (mock)'
      }),
      'pilula-sabedoria': () => ({
        success: true,
        agent: 'pilula-sabedoria',
        output: '💊 Píllula de Sabedoria (mock)'
      }),
      'checklist-cvm': () => ({
        success: true,
        agent: 'checklist-cvm',
        output: '✅ Validação CVM OK'
      })
    };

    const agent = agentMap[agentId];
    if (!agent) {
      return {
        success: false,
        error: `Agente não encontrado: ${agentId}`
      };
    }

    return agent();
  }

  async handleMorningCall() {
    console.log('🎬 TASK: Criar Morning Call');

    const rule = this.getRoutingRules('morning call');
    console.log(`📍 Sequência: ${rule.sequence}`);

    let output = '';
    let termometro = '';
    let pilula = '';

    // Step 1: Amorim
    const amorimResult = await this.executeAgent('amorim-analista', {});
    if (!amorimResult.success) {
      console.error('❌ Amorim falhou:', amorimResult.error);
      process.exit(1);
    }
    console.log('✅ Amorim: Análise completa');
    termometro = amorimResult.termometro;
    output += amorimResult.output + '\n';

    // Step 2: Nina
    const ninaResult = await this.executeAgent('redacao-9pilla', { termometro });
    if (!ninaResult.success) {
      console.error('❌ Nina falhou:', ninaResult.error);
      process.exit(1);
    }
    console.log('✅ Nina: Redação completa');
    output += ninaResult.output + '\n';

    // Step 3: Bela
    const belaResult = await this.executeAgent('pilula-sabedoria', {});
    if (!belaResult.success) {
      console.error('❌ Bela falhou:', belaResult.error);
      process.exit(1);
    }
    console.log('✅ Bela: Píllula pronta');
    pilula = belaResult.output;
    output += pilula + '\n';

    // Step 4: Léa (Compliance)
    const leaResult = await this.executeAgent('checklist-cvm', { content: output });
    if (!leaResult.success) {
      console.error('❌ Léa BLOQUEOU:', leaResult.error);
      process.exit(1);
    }
    console.log('✅ Léa: Compliance validado');

    // Validate constitution
    const issues = this.validateConstitution(output);
    if (issues.length > 0) {
      console.error('\n🚫 Constitution issues encontrados:');
      issues.forEach(issue => {
        console.error(`  - [${issue.type}] ${issue.message}`);
      });
      process.exit(1);
    }

    // Save output
    const today = new Date().toISOString().split('T')[0];
    const outputPath = path.join(CONTENT_DIR, 'morning-call', `${today}.md`);

    // Create directory if needed
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(outputPath, output);
    console.log(`\n✅ Morning Call salvo: ${outputPath}`);
    console.log('📤 Pronto para envio às 09h09');
  }

  async handleReel() {
    console.log('🎬 TASK: Criar Script de Reel');
    const rule = this.getRoutingRules('reel');
    console.log(`📍 Sequência: ${rule.sequence}`);
    console.log('⏳ Reel script generation (em desenvolvimento)');
  }

  async handleCopy() {
    console.log('🎬 TASK: Criar Copy de Produto');
    console.log('⏳ Copy product generation (em desenvolvimento)');
  }

  async handleMensagem() {
    console.log('🎬 TASK: Mensagem para Turma/VIP');
    console.log('⏳ Group message generation (em desenvolvimento)');
  }

  async handleSinal() {
    console.log('🎬 TASK: Gerar Sinal Privado');
    const rule = this.getRoutingRules('sinal');
    console.log(`📍 RESTRIÇÃO: ${rule.restriction}`);
    console.log('⏳ Private signal generation (em desenvolvimento)');
  }

  async run() {
    console.log('🤖 Caio Content Orchestrator v1.0.0\n');

    if (!this.task) {
      console.log('Uso: orchestrator.js <task>');
      console.log('Tasks disponíveis:');
      console.log('  - criar_morning_call');
      console.log('  - criar_reel_script');
      console.log('  - criar_copy_produto');
      console.log('  - mensagem_grupo');
      console.log('  - sinal_privado');
      process.exit(1);
    }

    try {
      switch (this.task) {
        case 'criar_morning_call':
          await this.handleMorningCall();
          break;
        case 'criar_reel_script':
          await this.handleReel();
          break;
        case 'criar_copy_produto':
          await this.handleCopy();
          break;
        case 'mensagem_grupo':
          await this.handleMensagem();
          break;
        case 'sinal_privado':
          await this.handleSinal();
          break;
        default:
          console.error(`❌ Task desconhecida: ${this.task}`);
          process.exit(1);
      }
    } catch (err) {
      console.error('❌ Erro durante execução:', err.message);
      process.exit(1);
    }
  }
}

// Execute
const orchestrator = new Orchestrator();
orchestrator.run().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
