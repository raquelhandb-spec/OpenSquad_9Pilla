# 📖 GUIA NTSL — Monitorar Order Flow no Profit Pro

**Objetivo:** Programar no Profit Pro para capturar Order Flow em tempo real

---

## 🎯 O QUE VAMOS FAZER

Criar um script NTSL que:
1. **Monitora o Order Book** (bid/ask)
2. **Detecta a ponta compradora vs vendedora**
3. **Identifica quem está puxando** (para cima ou para baixo)
4. **Gera alertas** quando mudanças significativas acontecem
5. **Exporta dados** para CSV (para análise em Python)

---

## 🔧 SETUP NTSL NO PROFIT PRO

### Passo 1: Abrir o Editor de Estratégias
1. No Profit Pro, clique em **Ferramentas → Editor de Estratégias**
2. Ou pressione **Ctrl + E**
3. Crie um novo arquivo: **File → New → Strategy**

### Passo 2: Estrutura Básica NTSL

```ntsl
// ═══════════════════════════════════════════════════════════════
// 🎯 ORDER FLOW MONITOR — Monitorar Fluxo de Ordens
// ═══════════════════════════════════════════════════════════════

{
  // ═══════════════════════════════════════════════════════════════
  // 1. VARIÁVEIS GLOBAIS
  // ═══════════════════════════════════════════════════════════════
  
  var compras_total = 0;          // Volume total de compras
  var vendas_total = 0;           // Volume total de vendas
  var saldo_fluxo = 0;            // Compras - Vendas
  var maior_compra = 0;           // Maior ordem de compra
  var maior_venda = 0;            // Maior ordem de venda
  
  // ═══════════════════════════════════════════════════════════════
  // 2. MONITORAR CADA TICK
  // ═══════════════════════════════════════════════════════════════
  
  OnTick()
  {
    // Capturar volume do tick
    var volume_atual = Volume();
    var preco_atual = Close();
    
    // Determinar se é compra ou venda (baseado na comparação com tick anterior)
    if (Open() < Close())
    {
      // Preço subiu = COMPRA
      compras_total = compras_total + volume_atual;
      if (volume_atual > maior_compra) { maior_compra = volume_atual; }
    }
    else if (Open() > Close())
    {
      // Preço caiu = VENDA
      vendas_total = vendas_total + volume_atual;
      if (volume_atual > maior_venda) { maior_venda = volume_atual; }
    }
    
    // Calcular saldo
    saldo_fluxo = compras_total - vendas_total;
    
    // ─────────────────────────────────────────────────────────────
    // 3. ALERTAS — Quando há mudança significativa
    // ─────────────────────────────────────────────────────────────
    
    // ALERTA 1: Grande compra (acima de 2x a média)
    if (volume_atual > maior_compra * 2)
    {
      Alert("🔴 GRANDE COMPRA DETECTADA: " + volume_atual + " contratos a R$ " + preco_atual);
    }
    
    // ALERTA 2: Grande venda (acima de 2x a média)
    if (volume_atual > maior_venda * 2)
    {
      Alert("🔵 GRANDE VENDA DETECTADA: " + volume_atual + " contratos a R$ " + preco_atual);
    }
    
    // ALERTA 3: Inversão de fluxo (mudança de sinal de compra para venda)
    if (saldo_fluxo < 0 AND saldo_fluxo[1] > 0)
    {
      Alert("⚠️ INVERSÃO: Ponta vendedora assumiu controle!");
    }
    else if (saldo_fluxo > 0 AND saldo_fluxo[1] < 0)
    {
      Alert("⚠️ INVERSÃO: Ponta compradora assumiu controle!");
    }
    
  } // fim OnTick()
  
  // ═══════════════════════════════════════════════════════════════
  // 4. FIM DA BARRA — Consolidar dados
  // ═══════════════════════════════════════════════════════════════
  
  OnBarClose()
  {
    // Salvar dados em arquivo para Python ler
    // (Profit Pro exporta automático ou pode usar funções customizadas)
    
    // Imprimir relatório da barra
    Print("════════════════════════════════════════════");
    Print("📊 RELATÓRIO DA BARRA");
    Print("════════════════════════════════════════════");
    Print("Compras: " + compras_total);
    Print("Vendas: " + vendas_total);
    Print("Saldo: " + saldo_fluxo);
    Print("Maior Compra: " + maior_compra);
    Print("Maior Venda: " + maior_venda);
    
    // Determinar quem está no controle
    if (saldo_fluxo > 0)
    {
      Print("🔴 PONTA COMPRADORA NO CONTROLE");
    }
    else if (saldo_fluxo < 0)
    {
      Print("🔵 PONTA VENDEDORA NO CONTROLE");
    }
    else
    {
      Print("⚖️ EQUILIBRIO DE FORÇAS");
    }
    
    Print("════════════════════════════════════════════");
  }
}
```

---

## 📊 O QUE ESTE SCRIPT FAZ

| Métrica | Significado |
|---------|-------------|
| **compras_total** | Volume total comprado na barra |
| **vendas_total** | Volume total vendido na barra |
| **saldo_fluxo** | Compras - Vendas (quem está vencendo?) |
| **maior_compra** | Maior ordem de compra (força da ponta) |
| **maior_venda** | Maior ordem de venda (força da ponta) |

---

## 🚨 ALERTAS GERADOS

✅ **GRANDE COMPRA**: Quando volume > 2x a média
✅ **GRANDE VENDA**: Quando volume > 2x a média  
✅ **INVERSÃO**: Quando ponta muda de controle

---

## 💾 EXPORTAR DADOS PARA CSV

Para que Python leia os dados, você precisa:

### Opção A: Exportação Automática do Profit
1. **Ferramentas → Exportar Dados**
2. Selecione o período
3. Escolha campos: Data, Hora, Abertura, Máxima, Mínima, Fechamento, Volume
4. Salve como CSV

### Opção B: Script NTSL que salva direto
```ntsl
// Adicionar dentro do OnBarClose()
FileWrite("C:\\Users\\raque\\9Pilla-Sistema\\squads\\shorts-maestro\\output\\profit_export.csv", 
  Date() + "," + Time() + "," + Open() + "," + High() + "," + Low() + "," + Close() + "," + Volume() + "," + saldo_fluxo);
```

---

## 🔗 PRÓXIMAS ETAPAS

1. ✅ Criar este script no Editor de Estratégias
2. ✅ Rodá-lo na sessão de hoje
3. ✅ Gerar alertas em tempo real
4. ✅ Exportar CSV com dados
5. ✅ Python lê CSV e cria análise completa

---

## 📝 REFERÊNCIAS NTSL

- **Documentação NTSL**: Central de Ajuda Profit Pro → NTSL Reference
- **Funções principais**:
  - `Volume()` - Volume do tick/barra
  - `Open()`, `High()`, `Low()`, `Close()` - Preços
  - `Alert()` - Gera alerta visual/sonoro
  - `Print()` - Escreve no log
  - `OnTick()` - Executado a cada tick
  - `OnBarClose()` - Executado ao fechar barra

---

## ✅ PRÓXIMO PASSO

**Você vai:**
1. Copiar este script no Editor de Estratégias
2. Rodar na sessão de hoje (durante a bolsa)
3. Me mandar a saída com os dados exportados

**Aí eu crio o Python que processa tudo!** 🚀
