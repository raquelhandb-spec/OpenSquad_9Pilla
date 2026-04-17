require('dotenv').config();
const fs = require('fs');
const path = require('path');

const { ZAPI_INSTANCE, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN, WHATSAPP_TEST_NUMBER, WHATSAPP_GROUP_ID } = process.env;

async function sendZapiMessage(phone, message) {
    if (!ZAPI_INSTANCE || !ZAPI_TOKEN) {
        console.error("ERRO: Credenciais ZAPI_INSTANCE ou ZAPI_TOKEN ausentes no arquivo .env");
        return;
    }

    const url = `https://api.z-api.io/instances/${ZAPI_INSTANCE}/token/${ZAPI_TOKEN}/send-text`;
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (ZAPI_CLIENT_TOKEN) {
        headers['Client-Token'] = ZAPI_CLIENT_TOKEN;
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                phone: phone,
                message: message
            })
        });

        const data = await response.json();
        console.log(`Z-API Response para ${phone}:`, data);
        return data;
    } catch (error) {
        console.error("Erro na requisição Z-API:", error.message);
    }
}

async function run() {
    const isGroup = process.argv.includes('--group');
    const targetNumber = isGroup ? WHATSAPP_GROUP_ID : WHATSAPP_TEST_NUMBER;
    const targetName = isGroup ? "Grupo 9Pilla" : "WhatsApp Pessoal";

    if (!targetNumber) {
        console.log(`Variável de destino não definida no .env para ${targetName}.`);
        return;
    }
    
    const draftPath = path.resolve(__dirname, '../../squads/morning-call/aquecimento.draft.md');
    const draftContent = fs.readFileSync(draftPath, 'utf8');
    
    console.log(`Enviando mensagem para: ${targetName} (${targetNumber})`);
    await sendZapiMessage(targetNumber, draftContent);
}

run();
