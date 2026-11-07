// Gera o ebook em PDF (A5): capa sem número + miolo numerado, sumário com páginas reais.
// Uso: node build.js  (requer playwright + poppler: pdftotext, pdfinfo, pdfunite)
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require('playwright');

const DIR = __dirname;
const SRC = path.join(DIR, 'src');
const OUT = path.join(DIR, 'Acoes-sem-Misterio-9Pilla.pdf');
const TMP = fs.mkdtempSync('/tmp/ebook-');

const parts = fs.readdirSync(SRC).filter((f) => f.endsWith('.html')).sort();
const full = parts.map((f) => fs.readFileSync(path.join(SRC, f), 'utf8')).join('\n');
const head = full.slice(0, full.indexOf('<body>') + 6);
const coverStart = full.indexOf('<section class="cover">');
const coverEnd = full.indexOf('</section>', coverStart) + 10;
const cover = full.slice(coverStart, coverEnd);
const bodyRest = full.slice(coverEnd);
const tocItems = [...bodyRest.matchAll(/data-toc="([^"]+)"/g)].map((m) => m[1]);
const chapNums = [...bodyRest.matchAll(/<div class="num">([^<]+)<\/div>/g)].map((m) => m[1]);
const chapTitles = [...bodyRest.matchAll(/<section class="chap"[^>]*>\s*<div class="num">[^<]*<\/div>\s*<h1>([^<]+)<\/h1>/g)].map((m) => m[1].replace(/&amp;/g,'&'));

function tocHtml(pages) {
  return tocItems
    .map((t, i) => {
      const n = chapNums[i] && chapNums[i].startsWith('Capítulo') ? chapNums[i].replace('Capítulo ', '') : '';
      return `<li><span><span class="c">${n}</span>${t}</span><span>${pages ? pages[i] : '00'}</span></li>`;
    })
    .join('\n');
}

const footer = `<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5pt;color:#8a93a3;padding:0 15mm;display:flex;justify-content:space-between"><span>Ações sem Mistério · 9Pilla</span><span class="pageNumber"></span></div>`;

async function render(page, html, file, withFooter) {
  await page.setContent(html, { waitUntil: 'load' });
  await page.pdf({
    path: file,
    width: '148mm',
    height: '210mm',
    printBackground: true,
    margin: withFooter ? { top: '17mm', bottom: '18mm', left: '15mm', right: '15mm' } : { top: 0, bottom: 0, left: 0, right: 0 },
    displayHeaderFooter: withFooter,
    headerTemplate: '<span></span>',
    footerTemplate: footer,
  });
}

function findPages(pdf) {
  const n = parseInt(execSync(`pdfinfo "${pdf}"`).toString().match(/Pages:\s+(\d+)/)[1], 10);
  const texts = [];
  for (let i = 1; i <= n; i++) texts.push(execSync(`pdftotext -f ${i} -l ${i} "${pdf}" -`).toString().replace(/\s+/g, ' '));
  let from = 0;
  return {
    n,
    pages: chapNums.map((num, i) => {
      for (let p = Math.max(from, 2); p < n; p++) {
        if (texts[p].includes(chapTitles[i])) {
          from = p + 1;
          return p + 1;
        }
      }
      return '?';
    }),
  };
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const coverHtml = head.replace('</style>', '.cover{margin:0!important;height:210mm}</style>') + cover + '</body></html>';
  await render(page, coverHtml, path.join(TMP, 'cover.pdf'), false);
  let bodyHtml = head + bodyRest.replace('@@TOC@@', tocHtml(null));
  await render(page, bodyHtml, path.join(TMP, 'body.pdf'), true);
  const { pages } = findPages(path.join(TMP, 'body.pdf'));
  bodyHtml = head + bodyRest.replace('@@TOC@@', tocHtml(pages));
  await render(page, bodyHtml, path.join(TMP, 'body.pdf'), true);
  const check = findPages(path.join(TMP, 'body.pdf'));
  await browser.close();
  execSync(`pdfunite "${TMP}/cover.pdf" "${TMP}/body.pdf" "${OUT}"`);
  console.log('Capítulos nas páginas:', check.pages.join(', '));
  console.log('Páginas do miolo:', check.n, '| total com capa:', check.n + 1);
})();
