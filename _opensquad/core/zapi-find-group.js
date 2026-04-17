require('dotenv').config();
const { ZAPI_INSTANCE, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN } = process.env;

async function findGroup() {
    if (!ZAPI_INSTANCE || !ZAPI_TOKEN) return;

    const headers = { 'Content-Type': 'application/json' };
    if (ZAPI_CLIENT_TOKEN) headers['Client-Token'] = ZAPI_CLIENT_TOKEN;

    const url = `https://api.z-api.io/instances/${ZAPI_INSTANCE}/token/${ZAPI_TOKEN}/groups`;
    
    try {
        console.log("Buscando lista completa de grupos na Z-API...");
        const response = await fetch(url, { headers });
        const data = await response.json();
        
        if (Array.isArray(data)) {
            console.log("\n--- GRUPOS ---");
            const turma = data.find(g => g.name.toUpperCase() === "TURMA-9PILLA" || g.name.includes("9PILLA"));
            if (turma) {
                console.log(`Grupo Encontrado: "${turma.name}" -> ID: ${turma.phone}`);
            } else {
                console.log("Grupo TURMA-9PILLA não encontrado na sincronização.");
                console.log("Outros grupos:", data.map(g => g.name).join(", "));
            }
        } else {
             console.log("Resposta:", data);
        }
    } catch (e) {
        console.error("Erro:", e.message);
    }
}

findGroup();
