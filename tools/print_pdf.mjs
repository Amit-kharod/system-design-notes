// Prints the notes page to an A4 PDF. Optionally saves PNGs of the first page and of every diagram for checking.
// usage: node tools/print_pdf.mjs <notes.html> <out.pdf> "<footer text>" [png prefix]
// Needs playwright-core (or playwright) with a Chromium: `npm i playwright-core && npx playwright install chromium`.
import path from 'path';
import { createRequire } from 'module';

async function chromiumLib() {
  for (const name of ['playwright-core', 'playwright']) {
    try { return (await import(name)).chromium; } catch (e) { /* try the next one */ }
  }
  const local = process.env.PLAYWRIGHT_DIR || path.join(process.cwd(), '/');
  return createRequire(local)('playwright-core').chromium;
}

const [html, pdf, footerText, png] = process.argv.slice(2);
const footer = (footerText || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const chromium = await chromiumLib();
const b = await chromium.launch();
const p = await b.newPage();
await p.goto('file://' + path.resolve(html));
await p.evaluate(() => document.fonts.ready);
await p.pdf({
  path: pdf, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
  footerTemplate: `<div style="width:100%;font-family:Helvetica;font-size:7.5px;color:#6b7a94;padding:0 15mm;display:flex;justify-content:space-between"><span>${footer}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
});
if (png) {
  await p.setViewportSize({ width: 1000, height: 1300 });
  await p.screenshot({ path: png + '-top.png' });
  const f = await p.$$('figure');
  for (let i = 0; i < f.length; i++) await f[i].screenshot({ path: `${png}-fig${i + 1}.png` });
}
await b.close();
console.log('pdf written:', pdf);
