require('dotenv').config();
const { ZAPI_INSTANCE, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN } = process.env;

async function listGroups() {
    if (!ZAPI_INSTANCE || !ZAPI_TOKEN) {
        console.error("ERRO: Credenciais ZAPI_INSTANCE ou ZAPI_TOKEN ausentes no arquivo .env");
        return;
    }

    const url = `https://api.z-api.io/instances/${ZAPI_INSTANCE}/token/${ZAPI_TOKEN}/chats`;
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (ZAPI_CLIENT_TOKEN) {
        headers['Client-Token'] = ZAPI_CLIENT_TOKEN;
    }

    try {
        console.log("Buscando lista de chats na Z-API...");
        const response = await fetch(url, {
            method: 'GET',
            headers: headers
        });

        const data = await response.json();
        
        if (Array.isArray(data)) {
            const groups = data.filter(chat => chat.isGroup);
            console.log("\n--- GRUPOS ENCONTRADOS ---");
            groups.forEach(g => console.log(`Nome: "${g.name}" -> ID: ${g.phone}`));
        } else {
            console.log("Retorno não esperado da API ao listar chats:", data);
        }
        
    } catch (error) {
        console.error("Erro na requisição Z-API:", error.message);
    }
}

listGroups();
