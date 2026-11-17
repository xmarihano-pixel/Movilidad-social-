// Exporta el reporte a PDF tamaño carta (espera a que MathJax termine).
// Uso: node reports/final/reporte/render_reporte.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'reporte.html'), { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise);
  await page.evaluate(() => MathJax.startup.promise);
  const errs = await page.evaluate(() => document.querySelectorAll('mjx-merror').length);
  console.log('errores MathJax:', errs);
  await page.pdf({ path: path.join(__dirname, 'Reporte_Final_Movilidad_Social.pdf'), format: 'Letter', printBackground: true,
                   displayHeaderFooter: true, headerTemplate: '<div></div>',
                   footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#666">¿Qué tan pegajosa es la pobreza? · UdeG–CUGDL · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                   margin: { top: '2cm', bottom: '2.1cm', left: '2cm', right: '2cm' } });
  await browser.close();
})();
