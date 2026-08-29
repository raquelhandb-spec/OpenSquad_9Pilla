# 🔐 SETUP: Google Sheets Privado com Senha

**Objetivo:** Planilha online com todas as credenciais, 100% privada e acessível 24/7

---

## 📋 **Passo-a-Passo (5 minutos)**

### **PASSO 1: Abrir Google Sheets**

1. Acesse: https://sheets.google.com
2. Clique em **"+ Planilha em branco"**
3. Dê nome: **"9PILLA-FERRAMENTAS-CREDENCIAIS"**

---

### **PASSO 2: Importar dados do CSV**

1. No Google Sheets aberto, clique em **Arquivo → Importar**
2. Selecione **"Upload"** e escolha o arquivo:
   ```
   FERRAMENTAS-CREDENCIAIS.csv
   ```
3. Clique em **"Localizar arquivo"** e abra
4. Selecione opção:
   ```
   ☑️ Substituir planilha
   ```
5. Clique em **"Importar dados"**

---

### **PASSO 3: Completar os dados**

A planilha virá com:
- ✅ Ferramentas essenciais (BRAPI, Claude, ElevenLabs, etc.) já preenchidas
- ⚠️ Campos "ADICIONAR" em ferramentas secundárias (Z-API, ManyChat, etc.)

**Complete manualmente:**
1. Adicione Login/Email (onde aplicável)
2. Adicione Senha (na coluna de Senha)
3. Adicione API Keys (na coluna de API_Key)
4. Atualize Status (Ativo/Pausado/Cancelar?)
5. Adicione Notas conforme necessário

---

### **PASSO 4: Proteger com Senha (Importante!)**

**Opção A: Proteger a planilha inteira**

1. Clique em **Dados → Proteger planilhas e intervalos**
2. Selecione **"Planilha"**
3. Clique em **"Defina permissões"**
4. Selecione:
   ```
   ☑️ Permitir que qualquer pessoa edite a planilha
       mas exigir autenticação
   ```
5. Clique em **"Feito"**

**Resultado:** Só você consegue abrir (Google autenticação)

---

**Opção B: Proteger com Senha Custom (Mais seguro)**

1. Na planilha, clique em **Arquivo → Fazer download → Excel (.xlsx)**
2. Salve no seu PC com nome:
   ```
   9PILLA-CREDENCIAIS-BACKUP.xlsx
   ```
3. Abra com Microsoft Excel
4. **Arquivo → Proteger Pasta de Trabalho → Proteger Pasta com Senha**
5. Digite sua senha
6. Salve
7. Delete o arquivo do PC (backup local guardado)

---

### **PASSO 5: Compartilhar Apenas com Você**

1. Na planilha Google Sheets, clique em **"Compartilhar"** (canto superior direito)
2. Remova qualquer compartilhamento existente
3. **Deixe como "Restrito"** → Apenas você tem acesso
4. Você pode acessar de qualquer lugar: https://sheets.google.com

---

## 🔐 **Segurança: Checklist**

```
☑️ Planilha criada em sua conta Google
☑️ Compartilhamento: Restrito (só você)
☑️ Autenticação Google: Ativa
☑️ Backup local: Salvo em .xlsx
☑️ URL privado: Apenas você consegue acessar
```

---

## 📱 **Acessar 24/7**

### **Do computador:**
```
https://sheets.google.com → Login Google → Abrir planilha
```

### **Do telefone:**
```
1. Instale app "Google Sheets"
2. Faça login com sua conta
3. Planilha aparece na lista
4. Acesse offline (sincroniza quando conecta)
```

---

## 🔄 **Manter Atualizado**

Toda semana (domingo):
```
☑️ Verificar Status de cada ferramenta
☑️ Atualizar senhas que mudaram
☑️ Adicionar novas ferramentas
☑️ Marcar o que cancelar
```

---

## 📊 **Estrutura da Planilha**

| Campo | Para quê | Exemplo |
|-------|---------|---------|
| **Categoria** | Agrupar ferramenta | Análise de Dados, IA, Trading |
| **Ferramenta** | Nome da tool | BRAPI, Claude, ElevenLabs |
| **Login/Email** | Usuário/email | nome@gmail.com |
| **Senha** | Acesso | ••••••••• (ocultar quando mostrar) |
| **API_Key** | Token de acesso | sk-ant-api03-... |
| **URL_Acesso** | Link direto | https://brapi.dev/api |
| **Função** | O que faz | Dados mercado, geração scripts |
| **Essencial?** | ✅ SIM / ❌ NÃO | Define prioridade |
| **Status** | Situação | Ativo/Pausado/Cancelar |
| **Notas** | Observações | Voice ID, Avatar ID, etc |

---

## ✨ **Pronto! Agora você tem:**

```
✅ Planilha online (Google Sheets)
✅ 100% privada (apenas você)
✅ Acessível 24/7 (qualquer dispositivo)
✅ Segura (autenticação Google + senha)
✅ Organizada (categorias, status, notas)
✅ Backup local (arquivo Excel)
```

---

## 🎯 **Use para:**

1. **Segunda-feira:** Verificar quais ferramentas rodam automático
2. **Domingo:** Revisar Status de cada uma
3. **Sempre:** Acessar credenciais quando precisar
4. **Planejamento:** Ver o que cancelar (Z-API, ManyChat, etc)

---

**Criada em:** 14/06/2026  
**Status:** 🟢 PRONTO PARA USAR  
**Segurança:** 🔐 Apenas você acessa

Qualquer dúvida no setup, chama! 💛
