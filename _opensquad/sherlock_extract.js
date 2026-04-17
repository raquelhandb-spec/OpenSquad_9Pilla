/**
 * Sherlock Instagram Extractor
 * Target: @warreninvestimentos
 * Mode: profile_1 (1 most recent post)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const TARGET_URL = 'https://www.instagram.com/warreninvestimentos/';
const SESSION_FILE = path.join(__dirname, '_browser_profile', 'instagram.json');
const OUTPUT_DIR = path.join(__dirname, '..', 'squads', 'noticias-financeiras', '_investigations', 'warreninvestimentos');

async function run() {
  // Ensure output directory exists
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const sessionExists = fs.existsSync(SESSION_FILE);
  console.log(`Session file exists: ${sessionExists}`);

  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox']
  });

  let context;
  if (sessionExists) {
    console.log('Loading existing session...');
    context = await browser.newContext({
      storageState: SESSION_FILE,
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      viewport: { width: 1280, height: 900 }
    });
  } else {
    console.log('No session found. Opening fresh browser...');
    context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      viewport: { width: 1280, height: 900 }
    });
  }

  const page = await context.newPage();

  console.log(`Navigating to ${TARGET_URL}...`);
  await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });

  // Wait for page to settle
  await page.waitForTimeout(4000);

  // Check if we need to log in
  const loginButton = await page.$('text=Log in');
  const isLoggedOut = loginButton !== null;
  console.log(`Is logged out: ${isLoggedOut}`);

  if (isLoggedOut) {
    console.log('Not logged in. Attempting to extract public content...');
  }

  // Take screenshot of profile
  const screenshotPath = path.join(OUTPUT_DIR, 'profile_screenshot.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log(`Profile screenshot saved: ${screenshotPath}`);

  // Extract profile data
  const profileData = await page.evaluate(() => {
    const data = {};

    // Try to get profile name
    const h1 = document.querySelector('h1, header h2');
    data.profileName = h1 ? h1.textContent.trim() : null;

    // Try to get bio
    const bio = document.querySelector('header section > div > span');
    data.bio = bio ? bio.textContent.trim() : null;

    // Try to get follower counts
    const stats = document.querySelectorAll('header section ul li');
    data.stats = Array.from(stats).map(li => li.textContent.trim());

    // Check page content
    data.pageTitle = document.title;
    data.url = window.location.href;

    return data;
  });

  console.log('Profile data:', JSON.stringify(profileData, null, 2));

  // Try to find posts in the grid
  const posts = await page.$$('article a[href*="/p/"], a[href*="/reel/"], div[class*="x1lliihq"] a[href*="/p/"]');
  console.log(`Found ${posts.length} post links`);

  // Also try alternate selectors
  const postLinks = await page.$$eval('a[href*="/p/"], a[href*="/reel/"]', (links) => {
    return links
      .map(a => ({
        href: a.href,
        img: a.querySelector('img') ? a.querySelector('img').src : null,
        alt: a.querySelector('img') ? a.querySelector('img').alt : null
      }))
      .filter(l => l.href && (l.href.includes('/p/') || l.href.includes('/reel/')))
      .slice(0, 5); // First 5 for inspection
  });

  console.log('Post links found:', JSON.stringify(postLinks, null, 2));

  let extractedPost = null;

  if (postLinks.length > 0) {
    const firstPostUrl = postLinks[0].href;
    console.log(`Navigating to first post: ${firstPostUrl}`);

    await page.goto(firstPostUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(4000);

    // Screenshot of post
    const postScreenshotPath = path.join(OUTPUT_DIR, 'post1_screenshot.png');
    await page.screenshot({ path: postScreenshotPath, fullPage: false });
    console.log(`Post screenshot saved: ${postScreenshotPath}`);

    // Extract post data
    extractedPost = await page.evaluate(() => {
      const data = {
        url: window.location.href,
        caption: null,
        date: null,
        likes: null,
        comments: null,
        type: 'unknown',
        slides: []
      };

      // Caption
      const captionSelectors = [
        'div[class*="caption"] span',
        'article div[class*="C4VMK"] span',
        'div[data-testid="post-comment-root-reply"] span',
        'h1',
        'article span',
        'div[class*="xdj266r"] span',
        'div._a9zs span',
        'div._a9zr span',
        'span[class*="caption"]',
      ];

      for (const sel of captionSelectors) {
        const el = document.querySelector(sel);
        if (el && el.textContent.trim().length > 10) {
          data.caption = el.textContent.trim();
          break;
        }
      }

      // Date
      const timeEl = document.querySelector('time');
      if (timeEl) {
        data.date = timeEl.getAttribute('datetime') || timeEl.textContent.trim();
      }

      // Likes
      const likeSelectors = [
        'section span[class*="like"]',
        'button[class*="like"] span',
        'span[class*="view"] span',
        'div[class*="Nm9Fw"] span',
        'a[href*="liked_by"] span',
      ];

      for (const sel of likeSelectors) {
        const el = document.querySelector(sel);
        if (el && el.textContent.trim()) {
          data.likes = el.textContent.trim();
          break;
        }
      }

      // Detect if carousel (multiple slides)
      const carouselDots = document.querySelectorAll('div[class*="carousel"] button, div[role="listitem"]');
      if (carouselDots.length > 1) {
        data.type = 'carousel';
      } else if (window.location.href.includes('/reel/')) {
        data.type = 'reel';
      } else {
        data.type = 'photo';
      }

      // Collect all visible text in the post
      const allText = [];
      document.querySelectorAll('article span, article p, article h1').forEach(el => {
        const text = el.textContent.trim();
        if (text.length > 5 && !allText.includes(text)) {
          allText.push(text);
        }
      });
      data.allText = allText;

      return data;
    });

    console.log('Post data:', JSON.stringify(extractedPost, null, 2));

    // If carousel, try to navigate slides
    if (extractedPost.type === 'carousel') {
      console.log('Detected carousel, navigating slides...');
      const slideTexts = [];

      for (let i = 0; i < 10; i++) {
        const slideText = await page.evaluate(() => {
          const imgs = document.querySelectorAll('article img[class*="x5yr21d"], article img');
          const text = [];
          imgs.forEach(img => {
            if (img.alt && img.alt.length > 5) {
              text.push(img.alt);
            }
          });
          return text;
        });
        slideTexts.push(...slideText);

        // Try clicking next button
        const nextBtn = await page.$('button[aria-label="Next"]');
        if (!nextBtn) break;
        await nextBtn.click();
        await page.waitForTimeout(1500);
      }

      extractedPost.slides = [...new Set(slideTexts)];
    }

    // Save session if not logged in
    if (!sessionExists) {
      // Check if now logged in
      const currentUrl = page.url();
      const isLoginPage = currentUrl.includes('/accounts/login');
      if (!isLoginPage) {
        fs.mkdirSync(path.dirname(SESSION_FILE), { recursive: true });
        await context.storageState({ path: SESSION_FILE });
        console.log(`Session saved to ${SESSION_FILE}`);
      }
    }
  }

  // Get full page text for fallback extraction
  const fullPageText = await page.evaluate(() => document.body.innerText);

  await browser.close();

  // Save raw extraction data
  const rawDataPath = path.join(OUTPUT_DIR, 'raw_extraction.json');
  fs.writeFileSync(rawDataPath, JSON.stringify({
    profileData,
    postLinks,
    extractedPost,
    fullPageText: fullPageText.substring(0, 5000), // First 5000 chars
    timestamp: new Date().toISOString()
  }, null, 2));

  console.log(`\nRaw extraction data saved: ${rawDataPath}`);

  return { profileData, postLinks, extractedPost, fullPageText };
}

run().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
