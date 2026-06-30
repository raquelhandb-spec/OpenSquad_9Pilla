#!/usr/bin/env node

/**
 * Route to Agent
 *
 * Roteia requisição para o agente correto baseado no task type
 * Invocado por Caio Orchestrator
 */

const agentId = process.argv[2];
const task = process.argv[3];
const inputData = process.argv[4] ? JSON.parse(process.argv[4]) : {};

const agents = {
  'amorim-editor': {
    name: 'Amorim Analista',
    tier: 1,
    role: 'Editorial Review + Market Analysis',
    activation: '@amorim-editor'
  },
  'nina-redacao': {
    name: 'Nina',
    tier: 1,
    role: 'Content Writer',
    activation: '@nina-redacao'
  },
  'lea-cvm': {
    name: 'Léa',
    tier: 2,
    role: 'Compliance Validator',
    activation: '@lea-cvm'
  },
  'bela-pilula': {
    name: 'Bela',
    tier: 2,
    role: 'Research & Wisdom Pills',
    activation: '@bela-pilula'
  },
  'caio-orchestrator': {
    name: 'Caio',
    tier: 0,
    role: 'Content Chief',
    activation: '@content-chief'
  }
};

function routeToAgent(agentId, task, input) {
  const agent = agents[agentId];

  if (!agent) {
    console.error(`❌ Agente não encontrado: ${agentId}`);
    process.exit(1);
  }

  console.log(`📍 Roteando para: ${agent.name} (Tier ${agent.tier})`);
  console.log(`   Role: ${agent.role}`);
  console.log(`   Ativação: ${agent.activation}`);

  // Em produção, isto invocaria via Claude API ou MCP
  // Aqui, simulamos com estrutura esperada

  const responses = {
    'amorim-editor': {
      task: 'criar_morning_call',
      output: `
📊 ANÁLISE DE MERCADO ESTRUTURADA
Fonte: BRAPI, Bloomberg, Valor Econômico

🌡️ Termômetro do Dia (${new Date().toLocaleDateString('pt-BR')})
| Ativo / Índice   | Cotação      | Var %  | Direção | Obs.                 |
|------------------|--------------|--------|---------|----------------------|
| Ibovespa         | 134.520 pts  | +0,42% | ▲       | Acima da mm21        |
| S&P 500          | 5.487 pts    | -0,18% | ▼       | Aguarda Fed          |
| Nasdaq           | 19.832 pts   | -0,31% | ▼       | Tech pressionada     |
| Petróleo Brent   | US$ 82,40    | +1,10% | ▲       | OPEC+ corta          |
| Petróleo WTI     | US$ 78,90    | +0,95% | ▲       |                      |
| Dólar (USD/BRL)  | R$ 5,22      | -0,30% | ▼       | BRL em recuperação   |
| PETR4            | R$ 38,70     | +0,80% | ▲       | Acompanha Brent      |
| VALE3            | R$ 61,20     | -0,50% | ▼       | Minério recua        |
| BOVA11           | R$ 134,15    | +0,38% | ▲       |                      |

Contexto Macro:
O cenário indica força residual no Ibovespa após gains em commodities.
Atenção para: PETR4 acompanha movimento positivo do Brent; VALE3 pressiona
em minério fraco; dólar recua com força do Real.

Volatilidade Implícita:
IV em nível médio. Mercado aguarda decisões do Federal Reserve e Copom.
      `
    },

    'nina-redacao': {
      task: 'criar_morning_call',
      output: `
☀️ Morning Call 9Pilla | Edição #${Math.floor(Math.random() * 500)} | ${new Date().toLocaleDateString('pt-BR')}

Bom dia Turma! Aqui é Raquel, vamos lá! Esse é o seu momento matinal mais
esperado... você provavelmente está no seu local de trabalho ou está se
preparando para trabalhar, então bora passar esse café juntos e sentar em
um local confortável para ler em 3 minutos o que vai mexer com seu dinheiro
nos próximos dias.

[Conteúdo estruturado com termômetro, 3 notícias, narrativa, píllula, fechamento]

Raquel Amorim | 9Pilla
Dinheiro não é destino. É a jornada para a LIBERDADE.

⚠️ Este conteúdo tem caráter exclusivamente educativo e informativo.
Não constitui recomendação de investimento, análise de valores mobiliários
ou consultoria financeira. Toda decisão de investimento é de responsabilidade
exclusiva do investidor. Investimentos envolvem riscos e podem resultar em perdas.
CVM Resolução 20/2021.
      `
    },

    'lea-cvm': {
      task: 'criar_morning_call',
      output: `✅ Léa: Aprovado para publicação

Validação concluída:
✓ Disclaimer CVM presente
✓ Nenhuma palavra banida detectada
✓ Raquel identificada como operadora de opções
✓ Conteúdo educacional (não sinal)
✓ Voice DNA coerente
✓ Ready para envio às 09h09
      `
    },

    'bela-pilula': {
      task: 'criar_morning_call',
      output: `💊 Píllula de Sabedoria | Livro

"Pai Rico, Pai Pobre" (Robert Kiyosaki)

O que você vai ganhar: Entender a diferença entre ativo e passivo.

"Os ricos não trabalham pelo dinheiro; fazem o dinheiro trabalhar por eles."

Este livro mudou a forma como milhões pensam sobre renda passiva e
criação de patrimônio. Simples, mas fundamental para quem quer construir
riqueza de verdade.
      `
    }
  };

  const response = responses[agentId];
  if (response) {
    console.log(`\n${response.output}\n`);
  } else {
    console.log(`\n[${agent.name} output para task: ${task}]\n`);
  }
}

if (!agentId) {
  console.error('Uso: route-to-agent.js <agentId> <task> [input]');
  process.exit(1);
}

routeToAgent(agentId, task, inputData);
