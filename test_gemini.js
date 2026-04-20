const https = require('https');

const API_KEY = process.env.GEMINI_API_KEY;

const options = {
  hostname: 'generativelanguage.googleapis.com',
  path: `/v1beta/models?key=${API_KEY}`,
  method: 'GET'
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    const json = JSON.parse(data);
    if (json.models) {
      json.models.forEach(m => console.log(m.name));
    } else {
      console.log(data);
    }
  });
});

req.on('error', (e) => console.error(e));
req.end();
