require('dotenv').config();
const fs = require('fs');
const path = require('path');

const { ZAPI_INSTANCE, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN, WHATSAPP_GROUP_ID } = process.env;

async function joinGroupAndSend() {
    if (!ZAPI_INSTANCE || !ZAPI_TOKEN) {
        console.error("ERRO: Credenciais ZAPI_INSTANCE ou ZAPI_TOKEN ausentes no arquivo .env");
        return;
    }

    const headers = {
        'Content-Type': 'application/json'
    };
    if (ZAPI_CLIENT_TOKEN) headers['Client-Token'] = ZAPI_CLIENT_TOKEN;

    // 1. Tentar resolver a URL de convite para obter o ID do Grupo
    console.log("Resolvendo Link de Convite na Z-API...");
    let groupId = null;
    
    // Se a variável WHATSAPP_GROUP_ID for um link de convite
    if (WHATSAPP_GROUP_ID && WHATSAPP_GROUP_ID.includes('chat.whatsapp.com')) {
        const joinUrl = `https://api.z-api.io/instances/${ZAPI_INSTANCE}/token/${ZAPI_TOKEN}/join-group`;
        try {
            const res = await fetch(joinUrl, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ invitationLink: WHATSAPP_GROUP_ID })
            });
            const data = await res.json();
            console.log("Retorno do Join Group:", data);
            
            // Geralmente Z-API retorna { groupId: "..." } ou similar
            groupId = data.phone || data.groupId || data.id; 
            
            if (!groupId && data.error) {
                console.log("Z-API falhou ao entrar pelo link de convite:", data.error);
                return;
            }
        } catch (error) {
            console.error("Erro na requisição Join Group:", error.message);
            return;
        }
    } else {
        groupId = WHATSAPP_GROUP_ID; // Se já for um ID direto
    }

    if (!groupId) {
        console.log("Não foi possível identificar o ID do grupo a partir do link de convite.");
        return;
    }

    console.log(`\nID resolvido do Grupo: ${groupId}`);
    
    // 2. Disparar a mensagem de aquecimento para o ID do Grupo resolvido
    const draftPath = path.resolve(__dirname, '../../squads/morning-call/aquecimento.draft.md');
    const draftContent = fs.readFileSync(draftPath, 'utf8');
    
    const sendUrl = `https://api.z-api.io/instances/${ZAPI_INSTANCE}/token/${ZAPI_TOKEN}/send-text`;
    try {
        console.log(`Enviando mensagem para o grupo (ID: ${groupId})...`);
        const response = await fetch(sendUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                phone: groupId,
                message: draftContent
            })
        });

        const sendData = await response.json();
        console.log("Z-API Response do envio ao Grupo:", sendData);
        
        // Vamos atualizar o .env com o ID numérico para os próximos disparos
        const envPath = path.resolve(__dirname, '../../.env');
        let envContent = fs.readFileSync(envPath, 'utf8');
        envContent = envContent.replace(WHATSAPP_GROUP_ID, groupId);
        fs.writeFileSync(envPath, envContent);
        console.log("\nID do grupo salvo no arquivo .env com sucesso!");
        
    } catch (error) {
        console.error("Erro no envio:", error.message);
    }
}

joinGroupAndSend();
