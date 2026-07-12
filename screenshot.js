const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const sizes = [
    { name: 'facebook-1200x630', w: 1200, h: 630 },
    { name: 'facebook-1080x1080', w: 1080, h: 1080 },
  ];

  for (const s of sizes) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: s.w, height: s.h } });
    await page.goto('https://com-bo-nau.vercel.app/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);

    const out = path.join('/root/projects/com-viet', `${s.name}.png`);
    await page.screenshot({ path: out, fullPage: false });
    console.log(`✅ Saved ${out} (${s.w}x${s.h})`);
    await browser.close();
  }
})();
