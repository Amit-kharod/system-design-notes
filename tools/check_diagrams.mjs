// Checks the diagrams the way the PDF draws them (Inter and JetBrains Mono from the series fonts):
//  - every text stays inside the diagram, with a small margin;
//  - every text inside a box (class "box") stays inside that box's rectangle;
//  - no two texts overlap.
// usage: node tools/check_diagrams.mjs [--png <dir>] <folder with .svg files> [more folders]
//        (exit code 1 when a problem is found; --png also saves a picture of every diagram, to look at)
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';

async function chromiumLib() {
  for (const name of ['playwright-core', 'playwright']) {
    try { return (await import(name)).chromium; } catch (e) { /* try the next one */ }
  }
  const local = process.env.PLAYWRIGHT_DIR || path.join(process.cwd(), '/');
  return createRequire(local)('playwright-core').chromium;
}

const FONTS = process.env.NOTES_FONTS || path.join(path.dirname(new URL(import.meta.url).pathname), '..', 'fonts');
const face = (fam, file) => fs.existsSync(path.join(FONTS, file))
  ? `@font-face{font-family:'${fam}';src:url(data:font/woff2;base64,${fs.readFileSync(path.join(FONTS, file)).toString('base64')}) format('woff2');font-weight:100 900}` : '';
const args = process.argv.slice(2);
const pi = args.indexOf('--png');
const pngDir = pi >= 0 ? args.splice(pi, 2)[1] : null;
const files = args.flatMap(d => fs.readdirSync(d).filter(f => f.endsWith('.svg')).sort().map(f => path.join(d, f)));
const html = `<!doctype html><html><head><meta charset="utf-8"><style>${face('Inter', 'inter.woff2')}${face('JetBrains Mono', 'jbm.woff2')}
body{margin:0;background:#fff} div{margin:10px}</style></head><body>${files.map(f => `<div data-name="${f}">${fs.readFileSync(f, 'utf8')}</div>`).join('')}</body></html>`;

const chromium = await chromiumLib();
const b = await chromium.launch();
const p = await b.newPage();
await p.setContent(html);
await p.evaluate(() => document.fonts.ready);
const report = await p.evaluate(() => {
  const out = [];
  for (const div of document.querySelectorAll('div[data-name]')) {
    const svg = div.querySelector('svg'), name = div.dataset.name.split('/').slice(-3).join('/');
    const W = svg.viewBox.baseVal.width, H = svg.viewBox.baseVal.height;
    const texts = [...svg.querySelectorAll('text')].map(t => ({ t, b: t.getBBox(), s: t.textContent.trim() }));
    for (const { b, s } of texts) {
      if (b.x < 8 || b.y < 4 || b.x + b.width > W - 8 || b.y + b.height > H - 4) out.push(`${name}: off the edge: "${s}"`);
    }
    for (const g of svg.querySelectorAll('g.box')) {
      const r = g.querySelector('rect').getBBox();
      for (const t of g.querySelectorAll('text')) {
        const bb = t.getBBox();
        if (bb.x < r.x + 2 || bb.x + bb.width > r.x + r.width - 2 || bb.y + 2 < r.y || bb.y + bb.height - 2 > r.y + r.height)
          out.push(`${name}: outside its box: "${t.textContent.trim()}"`);
      }
    }
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i].b, c = texts[j].b;
      const ox = Math.min(a.x + a.width, c.x + c.width) - Math.max(a.x, c.x);
      const oy = Math.min(a.y + a.height, c.y + c.height) - Math.max(a.y, c.y);
      if (ox > 1 && oy > 3) out.push(`${name}: texts overlap: "${texts[i].s}" / "${texts[j].s}"`);
    }
  }
  return out;
});
if (pngDir) {
  fs.mkdirSync(pngDir, { recursive: true });
  const divs = await p.$$('div[data-name]');
  for (let i = 0; i < divs.length; i++)
    await (await divs[i].$('svg')).screenshot({
      path: path.join(pngDir, path.basename(path.dirname(path.dirname(path.resolve(files[i])))).slice(0, 4) + '-' + path.basename(files[i], '.svg') + '.png'),
    });
}
await b.close();
console.log(`${files.length} diagrams checked, ${report.length} problems`);
for (const r of report) console.log('  ' + r);
process.exit(report.length ? 1 : 0);
