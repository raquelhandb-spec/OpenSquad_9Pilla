# 🎨 Padrões de Design 9Pilla — Extraído de 4 Referências Reais

**Data:** 14/06/2026  
**Baseado em:** Cal.com, Notion, Retool, GitBook  
**Status:** 🟢 Pronto para aplicar em landing page do ebook + infraestrutura 9Pilla

---

## 🔑 Padrão Emergente (Comum a Todas)

Cada plataforma reduz sobrecarga através de **3 camadas**:

```
CAMADA 1: CONTEXTO IMEDIATO
  ├─ Cal.com: data visível no calendário
  ├─ Notion: bloco selecionado em destaque
  ├─ Retool: painel contextual à direita
  └─ GitBook: página atual + breadcrumbs

CAMADA 2: DESCOBERTA PROGRESSIVA
  ├─ Cal.com: validação em camadas (client → server)
  ├─ Notion: templates como ponto de partida
  ├─ Retool: search contextual + progressive disclosure
  └─ GitBook: hierarquia visual + hints estruturados

CAMADA 3: AÇÃO SEM FRICÇÃO
  ├─ Cal.com: máximo 3 cliques até confirmação
  ├─ Notion: inline editing (click → edit → enter)
  ├─ Retool: grid snap + binding automático
  └─ GitBook: breadcrumb-jump direto ao tema
```

**Regra de Ouro:** Coloque o poder perto, esconda a complexidade, deixe o usuário decidir quando expandir.

---

## 1️⃣ CAL.COM — Agendamento Zero Fricção

### Padrões Replicáveis

| # | Padrão | Como Funciona | Aplicar em 9Pilla |
|---|--------|---------------|-------------------|
| **1** | Fluxo 3-etapas linear | Data/hora → Formulário → Confirmação. Nenhuma volta atrás. | Inscrição em cursos: Seleção → Dados → Pagamento |
| **2** | Time slots inline | Slots aparecem direto sob datas. Indisponíveis *disabled* (greyed). | Disponibilidade de mentorias visual |
| **3** | Validação em camadas | Client (blur/change) + form-wide + server-side pré-reserva. | Evitar race conditions em operações simultâneas |
| **4** | Calendário 3 layouts | Month/Week/Column. Usuário escolhe, nunca imposto. | Dashboard de operações com múltiplas vistas |
| **5** | Onboarding 4-step skippable | Perfil → Conectar → Disponibilidade → Link. Cada passo tangível. | Setup de conta: visível mas não bloqueante |

### Por que Funciona
Separação clara de concerns. Feedback visual que deixa claro o quê acontece a cada clique. Máximo 2-3 interações antes de submissão.

### Em 9Pilla
```
INSCRIÇÃO EM CURSO:
  Passo 1: Escolher turma (visual, calendário de datas)
  Passo 2: Dados (nome, email, experiência)
  Passo 3: Pagamento (PIX, cartão)
  Confirmação: Email + link para grupo
  → Máximo 5 cliques até estar no grupo!
```

---

## 2️⃣ NOTION — Produtividade com IA

### Padrões Replicáveis

| # | Padrão | Como Funciona | Aplicar em 9Pilla |
|---|--------|---------------|-------------------|
| **1** | Quiet Design (IA sugestiva) | IA sugere, não impõe. Blocos aparecem apenas quando contexto é claro. | Resumos automáticos de operações: "Adicionar resumo?" (não obrigatório) |
| **2** | Templates como ponte | Templates customizáveis eliminam síndrome página em branco. | "Novo relatório mensal" → template com seções prontas |
| **3** | Seleção constrained | Apenas 2 caminhos oferecidos (unidirecional vs bidirecional). | Relacionar leads com cursos: 1-N ou N-N (simples) |
| **4** | Drag-and-drop estrutural | Indentação é estrutural, não visual. Ícone 6-pontos + highlight azul subtil. | Organizar módulos de cursos por arrasto |
| **5** | Inline editing natural | Click/Tab ativa edição in-context. Esc reverte, Enter confirma. | Editar notas de operações sem modal popup |

### Por que Funciona
Coloca controle perto do contexto. Permite opções, não impõe. Resolve complexidade através de escolhas sucessivas.

### Em 9Pilla
```
BANCO DE LEADS + RESUMOS IA:
  1. Lead chega (planilha ou form)
  2. IA sugere: "Adicionar resumo automático?"
  3. Usuário clica → resumo gerado (inline)
  4. Edita direto no campo (sem modal)
  5. Relaciona com curso via dropdown constrained
  → Entrada fluida, sem síndrome de página em branco
```

---

## 3️⃣ RETOOL — 70+ Conectores Sem Caos

### Padrões Replicáveis

| # | Padrão | Como Funciona | Aplicar em 9Pilla |
|---|--------|---------------|-------------------|
| **1** | Progressive disclosure via abas | Abas (Add UI, Queries, Code, Release, Settings). Apenas contexto relevante visível. | Admin panel: Alunos | Operações | Financeiro | Reportes (abas) |
| **2** | Search contextual | Query builder com busca. Conectores frequentes recebem tratamento custom. | Buscar conectores (Brapi, ElevenLabs, HeyGen, Claude) por keyword |
| **3** | Inspector accordion + toggles | Seções (Content, Interaction, Appearance). Botão "Advanced" para raramente usados. | Painel direito mostra: Aprovação → Publicação → Agendamento (acordeão) |
| **4** | Canvas grid 12-col + snap | Componentes snapam durante resize/drag. Alinhamento visual, não matemático. | Dashboard de operações: grid responsivo, sem distorção |
| **5** | Binding visual (modelo reativo) | Two-way binding automático. Transformers JavaScript para extensibilidade. | Tabela de resultados ↔️ filtros: sincronização automática |

### Por que Funciona
Progressive disclosure + search contextual + accordion + grid snap = poder sem caos visual.

### Em 9Pilla
```
ADMIN PANEL CENTRAL:
  [Left Sidebar - Abas]
    ├─ Alunos (com busca: "encontre por email")
    ├─ Operações (grid com snap automático)
    ├─ Financeiro (tabelas reativas)
    └─ Reportes

  [Canvas Center]
    Tabela com 12-col grid, resize suave

  [Right Inspector]
    ├─ Content (nome, status)
    ├─ Interaction (on-click actions)
    └─ Advanced (custom JS se precisar)
```

---

## 4️⃣ GITBOOK — Documentação Design-First

### Padrões Replicáveis

| # | Padrão | Como Funciona | Aplicar em 9Pilla |
|---|--------|---------------|-------------------|
| **1** | Hierarquia visual 3 camadas | Sidebar (árvore aninhada) + Breadcrumbs (topo) + Outline (direita). Navegação clara. | Cursos: Módulo → Aula → Seção (sempre visível where you are) |
| **2** | Componentes padrão | Hints (info/success/warning/danger) + Code blocks + Tabs. Consistência visual. | "Dica de operação" (hint success), "Código de integração" (code block) |
| **3** | Embeds contextuais > links | YouTube, GitHub, Loom renderizam in-place (não link externo). | Videoaulas integradas nas páginas, não links |
| **4** | Search 2 modos | Quick Find (Cmd+K) local + Global Search. Resultado retorna match + link direto. | Buscar aulas por tema: local (dentro do curso) e global (todos cursos) |
| **5** | Sidebar estado persistente | localStorage salva expandido/colapsado. Não reabre estrutura toda sessão. | Usuário escolhe módulo favorito → permanece expandido |

### Por que Funciona
Minimiza fricção cognitiva. Sidebar sempre visível, estrutura cristalina, componentes consistentes.

### Em 9Pilla
```
DOCUMENTAÇÃO DE CURSOS:
  [Left Sidebar]
    Módulo 1 (expandido, estado salvo)
      ├─ Aula 1: Opções Básicas
      ├─ Aula 2: Estratégias
      └─ Quiz
    Módulo 2
      └─ ...

  [Top]
    Breadcrumbs: Cursos > Opções Intermediárias > Módulo 1 > Aula 1

  [Center]
    Texto + Hints ("atenção: volatilidade") + Vídeo embedded + Code (estratégia)

  [Right]
    Outline: H1 (Opções Básicas) + H2s (definição, exemplos)
```

---

## 📋 Resumo: Como Aplicar em 9Pilla (Roadmap)

### Imediato (Landing Page Ebook + Dashboard)
- ✅ **Cal.com pattern:** Inscrição em 3 etapas (fluxo visual simples)
- ✅ **Notion pattern:** Templates para novos relatórios, IA sugestiva
- ✅ **Retool pattern:** Admin panel com abas, search contextual
- ✅ **GitBook pattern:** Documentação com hierarquia clara

### Médio prazo (Infraestrutura 9Pilla)
- Dashboard de alunos (Retool grid 12-col)
- Banco de leads com IA (Notion inline editing)
- Agendamento de mentorias (Cal.com slots inline)
- Documentação de cursos (GitBook breadcrumbs + embeds)

### Longo prazo (Scaling)
- Command Palette (Cmd+K) para qualquer ação
- Binding reativo (Retool 2-way sync)
- Progressive disclosure (90+ features → 5 no contexto)

---

## 🎯 Aplicação na Landing Page do Ebook

**Padrões prioritários:**
1. **Cal.com:** CTA em 3 passos (simples, claro)
2. **GitBook:** Hierarquia visual de benefícios (breadcrumbs visuais)
3. **Notion:** Templates de "o que você vai aprender" (eliminação de dúvida)
4. **Retool:** Inspector colapsável (aprovações, bônus, desconto em acordeão)

---

**Próximo:** PROMPT-PERPLEXITY-EBOOK-LANDING.md (prompt MEGA-específico para Perplexity)

*Documentado por: Claude Code*  
*Session: 14/06/2026*
