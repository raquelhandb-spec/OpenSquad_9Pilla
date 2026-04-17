/**
 * Sherlock Instagram Extractor v3 — Correct Profiles
 * Squad: noticias-financeiras
 * Mode: profile_1 (1 most recent post per profile)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SESSION_FILE = path.join(__dirname, '_browser_profile', 'instagram.json');
const SQUAD = 'noticias-financeiras';
const BASE_DIR = path.join(__dirname, '..', 'squads', SQUAD, '_investigations');

const PROFILES = [
  'mepoupenaweb',
  'thiago.nigro',
  'primorico',
  'warrenbrasil',
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function extractProfile(page, username) {
  const outputDir = path.join(BASE_DIR, username);
  fs.mkdirSync(outputDir, { recursive: true });

  const url = `https://www.instagram.com/${username}/`;
  console.log(`\n===== @${username} =====`);
  console.log(`  Loading ${url}...`);

  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(5000);

  // Scroll to trigger lazy loading
  await page.evaluate(() => window.scrollBy(0, 400));
  await sleep(2000);
  await page.evaluate(() => window.scrollTo(0, 0));
  await sleep(1000);

  await page.screenshot({ path: path.join(outputDir, 'grid.png') });

  // Check for errors
  const bodyPreview = await page.evaluate(() => document.body.innerText.substring(0, 300));
  console.log(`  Page preview: ${bodyPreview.substring(0, 150).replace(/\n/g, ' ')}`);

  if (bodyPreview.includes('não está disponível') || bodyPreview.includes('not available')) {
    fs.writeFileSync(path.join(outputDir, 'error.md'),
      `# Error: @${username}\n\nProfile not available.\n\nPreview:\n${bodyPreview}`);
    console.log(`  ERROR: Profile not available`);
    return null;
  }

  if (bodyPreview.includes('perfil é privado') || bodyPreview.includes('private')) {
    fs.writeFileSync(path.join(outputDir, 'error.md'),
      `# Error: @${username}\n\nPrivate profile.\n\nPreview:\n${bodyPreview}`);
    console.log(`  ERROR: Private profile`);
    return null;
  }

  // Find post links
  const links = await page.evaluate(() => {
    const found = new Set();
    document.querySelectorAll('a[href]').forEach(a => {
      const h = a.href;
      if (h && (h.includes('/p/') || h.includes('/reel/')) && h.includes('instagram.com')) {
        found.add(h);
      }
    });
    return Array.from(found).slice(0, 10);
  });

  console.log(`  Found ${links.length} post links`);

  if (links.length === 0) {
    const fullBody = await page.evaluate(() => document.body.innerText.substring(0, 2000));
    fs.writeFileSync(path.join(outputDir, 'error.md'),
      `# Error: @${username}\n\nNo post links found.\n\nBody:\n${fullBody}`);
    console.log(`  ERROR: No links`);
    return null;
  }

  // Get most recent post (sort by post ID descending)
  const sortedLinks = [...links].sort((a, b) => {
    const getId = (u) => { const m = u.match(/\/(p|reel)\/([^/?]+)/); return m ? m[2] : ''; };
    return getId(b).localeCompare(getId(a));
  });

  const firstPostUrl = sortedLinks[0];
  console.log(`  Opening: ${firstPostUrl}`);

  await page.goto(firstPostUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(5000);

  await page.screenshot({ path: path.join(outputDir, 'post1.png') });

  const isReel = firstPostUrl.includes('/reel/');

  // Extract post data
  const post = await page.evaluate((isReel) => {
    const data = {
      url: window.location.href,
      type: isReel ? 'reel' : 'photo',
      date: '',
      caption: '',
    };

    const timeEl = document.querySelector('time');
    if (timeEl) data.date = timeEl.getAttribute('datetime') || timeEl.innerText?.trim();

    const nextBtn = document.querySelector('button[aria-label="Next"], button[aria-label="Próximo"]');
    if (nextBtn) data.type = 'carousel';

    const article = document.querySelector('article, main');
    data.articleText = article ? article.innerText?.substring(0, 6000) : document.body.innerText.substring(0, 6000);

    return data;
  }, isReel);

  // Navigate carousel
  const slides = [];
  if (post.type === 'carousel') {
    console.log(`  Navigating carousel...`);
    for (let i = 1; i <= 15; i++) {
      const imgAlts = await page.evaluate(() =>
        Array.from(document.querySelectorAll('article img'))
          .map(img => img.alt?.trim())
          .filter(t => t && t.length > 5)
      );
      slides.push({ slide: i, texts: imgAlts });
      await page.screenshot({ path: path.join(outputDir, `slide${i}.png`) });

      const nextBtn = await page.$('button[aria-label="Next"], button[aria-label="Próximo"]');
      if (!nextBtn) { console.log(`  Last slide: ${i}`); break; }
      await nextBtn.click();
      await sleep(1500);
    }
  }

  const result = { username, post: { ...post, slides } };
  fs.writeFileSync(path.join(outputDir, 'raw_extraction.json'), JSON.stringify(result, null, 2));
  console.log(`  Saved raw_extraction.json (type: ${post.type}, slides: ${slides.length})`);
  return result;
}

async function run() {
  console.log('Sherlock v3 — Correct handles');
  console.log(`Profiles: ${PROFILES.join(', ')}\n`);

  const browser = await chromium.launch({ headless: false, args: ['--no-sandbox'] });
  const context = await browser.newContext({
    storageState: SESSION_FILE,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 900 },
  });

  const page = await context.newPage();
  const results = [];

  for (const username of PROFILES) {
    try {
      const result = await extractProfile(page, username);
      if (result) results.push(result);
    } catch (err) {
      console.error(`  Error @${username}: ${err.message}`);
      const outDir = path.join(BASE_DIR, username);
      fs.mkdirSync(outDir, { recursive: true });
      fs.writeFileSync(path.join(outDir, 'error.md'), `# Error: @${username}\n\n${err.message}`);
    }
    await sleep(3000);
  }

  await browser.close();
  console.log(`\n===== DONE: ${results.length}/${PROFILES.length} extracted =====`);
  results.forEach(r => console.log(`  @${r.username}: ${r.post.type}, slides: ${r.post.slides?.length || 0}`));
}

run().catch(err => { console.error('Fatal:', err); process.exit(1); });
