// Exporta el cartel a PDF (90 × 120 cm) y a una vista previa PNG.
// Uso: node reports/final/cartel/render_cartel.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const W = Math.round(90 / 2.54 * 96), H = Math.round(120 / 2.54 * 96);
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.goto('file://' + path.join(dir, 'cartel.html'));
  await page.waitForLoadState('networkidle');
  // Revisión de desbordes: secciones cuyo contenido no cabe
  const over = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('section, .poster, main, footer').forEach(el => {
      if (el.scrollHeight > el.clientHeight + 2) out.push((el.querySelector('h3')?.innerText || el.className) + ': +' + (el.scrollHeight - el.clientHeight) + 'px');
    });
    const p = document.querySelector('.poster');
    out.push('alto contenido ' + p.scrollHeight + ' / ' + p.clientHeight);
    return out;
  });
  console.log(over.join('\n'));
  await page.pdf({ path: path.join(dir, 'cartel_90x120.pdf'), width: '90cm', height: '120cm', printBackground: true });
  await page.screenshot({ path: path.join(dir, 'cartel_vista_previa.png'), scale: 'css' });
  await browser.close();
})();
