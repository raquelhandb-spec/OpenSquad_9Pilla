# Guia de Implementação: 5 Padrões de Design do Retool
## Exemplos Práticos e Comparações Before/After

---

## PADRÃO 1: Organização de Conectores (Categorização + Busca)

### ANTES (Caótico)
```
Data Sources
├── PostgreSQL
├── MySQL
├── MongoDB
├── Stripe
├── Google Sheets
├── Salesforce
├── Slack
├── Twitter
├── REST API
├── GraphQL
├── Webhooks
├── Redis
├── Elasticsearch
... [70+ mais sem categorização]
```
❌ Usuário com 100 integrações possíveis se perde  
❌ Não sabe se precisa "Database" ou "Cloud Service"

### DEPOIS (Retool)
```
INTEGRATIONS
├── 📊 DATABASES (15)
│   ├── PostgreSQL
│   ├── MySQL
│   ├── MongoDB
│   └── [+ 12 mais]
│
├── 🔌 APIs (12)
│   ├── REST API
│   ├── GraphQL
│   └── [+ 10 mais]
│
├── ☁️ CLOUD SERVICES (20)
│   ├── Google Sheets
│   ├── Salesforce
│   ├── Stripe
│   └── [+ 17 mais]
│
└── 🏢 ENTERPRISE (18)
    ├── SAP
    ├── ServiceNow
    └── [+ 16 mais]
```

**Busca contextual:**
```
User types "stripe" → 
1. Stripe (Cloud Service)
   📝 28 docs | 💬 156 community examples

2. Payment integrations (category)
   → Stripe, Square, PayPal, Razorpay
```

✅ Usuário encontra em 3 cliques  
✅ Documentação integrada  
✅ Exemplos comunitários visíveis

### Por Que Isso Importa
- **Escalabilidade mental:** Categorias = chunks cognitivos
- **Reduced cognitive load:** "preciso de banco de dados" é subcategoria clara
- **Discoverability:** Vendo "Cloud Services" pode descobrir Stripe quando procurava Google Sheets

### Para Implementar (Tech Stack)
```javascript
// Dados de exemplo
const connectors = [
  {
    id: 'postgres',
    name: 'PostgreSQL',
    category: 'databases',
    tags: ['sql', 'relational', 'open-source'],
    popularity: 95,
    docs_count: 45
  },
  {
    id: 'stripe',
    name: 'Stripe',
    category: 'cloud_services',
    tags: ['payments', 'saas'],
    popularity: 88,
    docs_count: 32
  },
  // ...
];

// Interface
<ConnectorBrowser 
  connectors={connectors}
  groupBy="category"
  enableSearch={true}
  enableTags={true}
/>
```

---

## PADRÃO 2: Editor Visual com Estado Sincronizado

### ANTES (Desincronizado)
```
Canvas                          Explorer                      Inspector
┌──────────────────────┐        ┌──────────────┐             ┌──────────┐
│                      │        │ Components   │             │ Props    │
│   [Button] [Text]    │        │  - Form      │             │ Color:__ │
│                      │        │    - Input1  │             │ Size: __ │
│ User selects button  │        │    - Button  │             │          │
│ no canvas            │        │              │             │          │
└──────────────────────┘        └──────────────┘             └──────────┘
                    ❌ Seleção não aparece no Explorer
                    ❌ Mudar props em um lugar não atualiza outro
```

### DEPOIS (Retool com Redux)
```
Canvas                          Explorer                      Inspector
┌──────────────────────┐        ┌──────────────┐             ┌──────────┐
│                      │        │ Components   │             │ Props    │
│   [Button] [Text]    │        │  - Form      │             │ Color:__ │
│   ▲ Selected ▲       │        │    - Input1  │             │ Size: __ │
│                      │        │    - Button  │             │ Font:__  │
│ User selects button  │        │      ◀ ▶ ▶   │             │          │
│                      │        │              │             │          │
└──────────────────────┘        └──────────────┘             └──────────┘
         │                           │                            │
         └──────────┬────────────────┼────────────────────────────┘
                    ↓
              Redux Store
         state.selectedComponent = "Button"
         state.Button.props = {color: '...', size: '...'}
         
User edits color in Inspector → Redux dispatches action → 
  Canvas re-renders AND Explorer updates simultaneously
```

✅ **ACID property:** Uma mudança = sincronização em tempo real  
✅ **State is source of truth:** Nunca diverge  
✅ **DevTools:** Redux DevTools mostra toda história de mudanças

### Diagrama de Fluxo Detalhado
```
USER ACTION (ex: click button no canvas)
    ↓
DISPATCH (action: 'SELECT_COMPONENT', payload: 'Button')
    ↓
REDUCER (state.selectedComponent = 'Button')
    ↓
STORE UPDATE (subscribers notificados)
    ↓
RE-RENDER TUDO
    ├─ Canvas: destaca Button visualmente
    ├─ Explorer: scroll para Button, mostra como selecionado
    └─ Inspector: mostra props de Button
```

### Para Implementar (React + Redux)
```javascript
// Store reducer (simplificado)
const editorReducer = (state, action) => {
  switch (action.type) {
    case 'SELECT_COMPONENT':
      return {
        ...state,
        selectedComponentId: action.payload,
        inspectorVisible: true
      };
    
    case 'UPDATE_COMPONENT_PROP':
      return {
        ...state,
        components: {
          ...state.components,
          [state.selectedComponentId]: {
            ...state.components[state.selectedComponentId],
            props: {
              ...state.components[state.selectedComponentId].props,
              [action.key]: action.value
            }
          }
        }
      };
    
    default:
      return state;
  }
};

// Subscribers (connected components)
const CanvasComponent = ({ selectedId, dispatch }) => (
  <div onClick={(e) => dispatch({ type: 'SELECT_COMPONENT', payload: e.target.id })}>
    {/* render canvas */}
  </div>
);

const InspectorPanel = ({ selectedComponent, dispatch }) => (
  <div>
    <input 
      value={selectedComponent.props.color}
      onChange={(e) => dispatch({ 
        type: 'UPDATE_COMPONENT_PROP', 
        key: 'color', 
        value: e.target.value 
      })}
    />
  </div>
);
```

---

## PADRÃO 3: Discovery via Command Palette + Categorização

### ANTES (Navegação por Menu)
```
1. Usuário quer encontrar componente "Table"
2. Abre menu "Components"
3. Procura categoria correta (talvez "Display"? "Data"?)
4. Scroll até encontrar
5. Clica

⏱️ 20-30 segundos por ação
```

### DEPOIS (Retool Command Palette)
```
1. Press: Cmd+K
2. Type: "table"
3. See instant results:
   ├─ Table (component)
   ├─ Export to Excel (action)
   └─ Refresh table data (query action)
4. Press Enter

⏱️ 2-3 segundos por ação
```

### Visual do Command Palette
```
┌─────────────────────────────────────────────────────────┐
│  Cmd+K          [Search components, actions, queries...] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Recent                                                   │
│ ├─ Run query: fetchUsers                                │
│ └─ Select: Button1                                       │
│                                                          │
│ COMPONENTS (matching "tabl")                            │
│ ├─ 📊 Table                                              │
│ │  └─ Insert into Canvas                                │
│ └─ Text (1 match in name)                               │
│                                                          │
│ ACTIONS (matching "tabl")                               │
│ ├─ Export Table to CSV                                   │
│ └─ Refresh table data                                    │
│                                                          │
│ QUERIES (matching "tabl")                               │
│ └─ fetchTableData                                        │
│                                                          │
│ [Cmd+K = Toggle | ↑↓ Navigate | Enter = Execute]       │
└─────────────────────────────────────────────────────────┘
```

### Categorização Interna (Data Retool)
```javascript
const commandPaletteItems = [
  // ACTIONS (executáveis)
  { type: 'action', label: 'New Query', icon: '⚙️', fn: createQuery },
  { type: 'action', label: 'Save App', icon: '💾', fn: saveApp },
  
  // COMPONENTS (inseríveis)
  { type: 'component', label: 'Table', icon: '📊', fn: addComponent },
  { type: 'component', label: 'Button', icon: '🔘', fn: addComponent },
  
  // CODE (navigáveis)
  { type: 'code', label: 'query_fetchUsers', icon: '📝', fn: selectQuery },
  
  // Filtrado por busca fuzzy
];

// Fuzzy search (exemplo: "tbl" → "Table")
const fuse = new Fuse(commandPaletteItems, { keys: ['label'] });
const results = fuse.search('tbl'); // encontra "Table"
```

### Por Que Cada Categoria
- **ACTIONS:** "Quero fazer algo" (New, Save, Deploy)
- **COMPONENTS:** "Quero inserir algo" (Button, Table, Modal)
- **CODE:** "Quero editar algo" (queryName, functionName)

---

## PADRÃO 4: Progressive Disclosure (Inspector em Três Atos)

### ANTES (Esmagador)
```
Component Properties
├─ Label: ________________
├─ Placeholder: ________________
├─ Default value: ________________
├─ Pattern: ________________
├─ Disabled: [ ]
├─ Hidden: [ ]
├─ Min length: ________________
├─ Max length: ________________
├─ Regex: ________________
├─ Error message: ________________
├─ Tooltip: ________________
├─ Color: [color picker]
├─ Background color: [color picker]
├─ Border width: ________________
├─ Border color: [color picker]
├─ Border radius: ________________
├─ Padding: ________________
├─ Font family: ________________
├─ Font size: ________________
├─ Font weight: ________________
├─ Text color: ________________
├─ Text align: ________________
├─ Width: ________________
├─ Height: ________________
└─ ... [30 mais propriedades]

User: "Onde está o que eu preciso?"
```

### DEPOIS (Retool Progressive Disclosure)
```
┌─────────────────────────────────────┐
│ Text Input Properties               │
├─────────────────────────────────────┤
│ 📋 CONTENT  |  ⚡ INTERACTION  | 🎨 APPEARANCE │
├─────────────────────────────────────┤
│ [CONTENT SELECTED]                  │
├─────────────────────────────────────┤
│ □ Label                             │
│ □ Placeholder                       │
│ □ Default value                     │
│ □ Disabled state                    │
│ □ Hidden                            │
│ ... [+5 mais]                       │
│ [▼ Advanced]                        │ ← click para pattern, regex, etc.
└─────────────────────────────────────┘

User: "Content = dados do componente. Encontrei. Pronto."
```

### Estrutura das Três Abas

| ABA | CONTEÚDO | CASOS TÍPICOS |
|-----|----------|---------------|
| **CONTENT** | Label, placeholder, default value, options (select), format (currency) | 95% das edições |
| **INTERACTION** | onChange, onClick, validation rules, event handlers, disabled logic | 4% das edições |
| **APPEARANCE** | Color, size, padding, border, font, hidden state | 1% das edições |

### Padrão de List Editing (Add-ons, Validations, Styles)
```
Validation Rules (INTERACTION tab)
┌─────────────────────────────────────┐
│ Validation Rules                    │
├─────────────────────────────────────┤
│ [+ Add validation rule]             │
│                                     │
│ Rule 1: Required                    │
│ ├─ Condition: !self.value          │
│ └─ [Remove]                         │
│                                     │
│ Rule 2: Min length                  │
│ ├─ Condition: self.value.length < 3│
│ └─ [Remove]                         │
│                                     │
│ [+ Add validation rule]             │
└─────────────────────────────────────┘

User escolhe (progressivamente) o que precisa:
- Começou com 0
- Adicionou "Required" (clicou +)
- Depois adicionou "Min length" (clicou + novamente)
- Não vê as 20 validações que não usa
```

### Para Implementar (React)
```javascript
const InspectorPanel = ({ component }) => {
  const [activeTab, setActiveTab] = useState('content');
  const [advancedExpanded, setAdvancedExpanded] = useState(false);

  const contentProperties = [
    { label: 'Label', key: 'label', required: true },
    { label: 'Placeholder', key: 'placeholder' },
    { label: 'Default value', key: 'defaultValue' },
    { label: 'Disabled', key: 'disabled' },
    // ... [5 mais comuns]
  ];

  const advancedProperties = [
    { label: 'Pattern (Regex)', key: 'pattern' },
    { label: 'Min length', key: 'minLength' },
    { label: 'Max length', key: 'maxLength' },
    // ... [10 mais raros]
  ];

  return (
    <div className="inspector">
      <Tabs value={activeTab} onChange={setActiveTab}>
        <Tab label="CONTENT" value="content" />
        <Tab label="INTERACTION" value="interaction" />
        <Tab label="APPEARANCE" value="appearance" />
      </Tabs>

      {activeTab === 'content' && (
        <div>
          {contentProperties.map(prop => (
            <PropertyField key={prop.key} {...prop} />
          ))}
          
          <div className="advanced-section">
            <button onClick={() => setAdvancedExpanded(!advancedExpanded)}>
              {advancedExpanded ? '▼' : '▶'} Advanced
            </button>
            
            {advancedExpanded && advancedProperties.map(prop => (
              <PropertyField key={prop.key} {...prop} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

---

## PADRÃO 5: Visual Data Binding (Dependency Graph + Transformers)

### ANTES (Spaghetti Code)
```javascript
// Onde Table1.data vem de? Quem depende dela?
// Arquivo de 500 linhas... procurando por "Table1"...
// Encontra em 3 lugares diferentes com lógicas desconexas

// query_fetchUsers roda? Quando? Por quê?
// Tem 7 event handlers que podem disparar
```

### DEPOIS (Retool com Dependency Graph)
```
Visual Dependency Graph
┌────────────────────────────────────────┐
│ Selected: query_fetchUsers             │
├────────────────────────────────────────┤
│ DEPENDENTS (Quem usa isso?)           │
│ ├─ Table1.data                        │
│ ├─ Button_Export (condicional)        │
│ ├─ Chart1.series                      │
│ └─ TextInput_Count.value              │
│                                        │
│ DEPENDENCIES (Do que depende?)        │
│ ├─ TextInput_Search.value (WHERE)     │
│ ├─ SelectBox_Status.value (WHERE)     │
│ └─ Pagination.pageNumber (LIMIT)      │
└────────────────────────────────────────┘

Hover sobre item → mostra ligação no canvas
Clica → navega para aquele componente/query
```

### Fluxo de Dados Visual (com Transformers)
```
┌─────────────────┐
│  SQL Query      │
│  SELECT * FROM  │
│  users WHERE    │
│  id = ?         │
└────────┬────────┘
         │ [executa]
         ↓
┌─────────────────┐
│ Raw Data        │
│ [{              │
│   id: 1,        │
│   birthDate:    │
│   "1990-01-01"  │
│ }]              │
└────────┬────────┘
         │ [transformer JS]
         ↓
┌─────────────────────────────┐
│ TRANSFORMER                 │
│ return data.map(user => ({  │
│   ...user,                  │
│   age: calculateAge(        │
│     user.birthDate          │
│   ),                        │
│   displayName:              │
│     user.name.toUpperCase() │
│ }))                         │
└────────┬────────────────────┘
         │
         ↓
┌────────────────────┐
│ Transformed Data   │
│ [{                 │
│   id: 1,           │
│   birthDate: "...",│
│   age: 34,         │
│   displayName:     │
│   "JOHN DOE"       │
│ }]                 │
└────────┬───────────┘
         │ [alimenta componente]
         ↓
┌────────────────────┐
│ Table1             │
│ [mostra 3 colunas] │
│ id | displayName   │
│ age                │
└────────────────────┘
```

### Event Handler Visual Flow
```
Button "Export CSV"
│
├─ ON CLICK:
│  ├─ Run: query_validateUser [sync]
│  │  └─ IF SUCCESS:
│  │     ├─ Run: query_exportCSV [then]
│  │     │  └─ IF SUCCESS:
│  │     │     ├─ Show: Toast "Exported!" [then]
│  │     │     └─ Download: blob [then]
│  │     │
│  │     └─ IF ERROR:
│  │        └─ Show: Toast "Validation failed" [then]
│  │
│  └─ IF ERROR:
│     └─ Show: Toast error.message [then]
│
└─ WHILE RUNNING:
   └─ Disable button (visual feedback)
```

### Para Implementar (Query + Transformer)
```javascript
// Query com transformer
const query = {
  id: 'fetchUsers',
  type: 'sql',
  sql: 'SELECT * FROM users WHERE status = ? LIMIT ?',
  params: [
    SelectBox_Status.value,
    Pagination.pageSize
  ],
  
  // TRANSFORMER: código JS que executa DEPOIS da query
  transformer: `
    return data.map(user => ({
      ...user,
      age: Math.floor((Date.now() - new Date(user.birthDate)) / 31536000000),
      displayName: user.firstName + ' ' + user.lastName,
      isOld: user.age > 60
    }))
  `,
  
  cacheDurationSeconds: 300
};

// Visualização
<QueryEditor 
  query={query}
  previewData={rawData}
  transformedData={transformedData}
  showDependencyGraph={true}
/>
```

---

## CHECKLIST DE IMPLEMENTAÇÃO PRIORIZADA

### Fase 1 (Semanas 1-2) — MVP
- [ ] Redux store com state global
- [ ] Canvas + Explorer + Inspector sincronizados
- [ ] Command Palette (Cmd+K) com 20 ações básicas
- [ ] Inspector em 2 abas: Content + Advanced

### Fase 2 (Semanas 3-4) — Profissional
- [ ] Progressive disclosure (Content/Interaction/Appearance)
- [ ] Dependency graph visualization
- [ ] Categorização de integrações (se aplicável)
- [ ] Busca fuzzy em Command Palette

### Fase 3 (Semanas 5+) — Avançado
- [ ] Query transformers visuais
- [ ] Visual event handler flow
- [ ] Advanced collapse com propriedades raramente usadas
- [ ] Integration marketplace com documentação integrada

---

## MÉTRICAS QUE INDICAM SUCESSO

Ao implementar esses padrões, procure por:

| Métrica | Antes | Depois | Alvo |
|---------|-------|--------|------|
| Tempo médio para achar componente | 30s | 5s | <3s |
| Cliques por ação no editor | 5-7 | 2-3 | <2 |
| Users usando Command Palette | 0% | 60%+ | 80%+ |
| Support tickets "como faço X?" | Alto | Médio | Baixo |
| Feature discovery (% users sabem de feature) | 40% | 70% | 90%+ |

---

## CONCLUSÃO

Esses cinco padrões funcionam porque respeitam **princípios fundamentais:**

1. **Sincronização** (Pattern 2) → Confiança no sistema
2. **Categorização** (Pattern 1) → Reduz carga cognitiva
3. **Discoverability** (Pattern 3) → Power users + beginners
4. **Progressive disclosure** (Pattern 4) → Escalável
5. **Visual causality** (Pattern 5) → Rastreabilidade

Juntos, permitem que um designer gerencie **100+ componentes + 50+ integrações + 500+ queries** sem parecer caótico.
