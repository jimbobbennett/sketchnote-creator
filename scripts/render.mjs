#!/usr/bin/env node
/* Render a sketchnote layout.json -> PNG (+ SVG) using rough.js + Playwright.
   Usage: node render.mjs <layout.json> [--out <basename>] [--no-svg] [--scale N] [--keep-html]
   Phase 1: implements the `grid` layout. Other layouts fall back to grid for now. */
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve, basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');

// ---------- args ----------
const args = process.argv.slice(2);
if (!args[0] || args[0].startsWith('--')) {
  console.error('usage: node render.mjs <layout.json> [--out <basename>] [--no-svg] [--scale N] [--keep-html]');
  process.exit(2);
}
const inputPath = resolve(args[0]);
const flag = (name) => args.includes(name);
const opt = (name, dflt) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : dflt; };
const outBase = resolve(opt('--out', join(dirname(inputPath), basename(inputPath).replace(/\.json$/, ''))));
const emitSvg = !flag('--no-svg');
const scale = Number(opt('--scale', '2'));
const keepHtml = flag('--keep-html');

// ---------- palette ----------
const HUES = { teal: '#008394', indigo: '#7582FF', purple: '#8B4FD4', magenta: '#C2266F', pink: '#EA338A' };
const HUE_CYCLE = ['teal', 'indigo', 'purple', 'magenta'];
const ACCENT = '#EA338A';

// ---------- load ----------
const layout = JSON.parse(readFileSync(inputPath, 'utf8'));
const css = readFileSync(join(ROOT, 'templates', 'sketchnote.css'), 'utf8');
const drawJs = readFileSync(join(ROOT, 'templates', 'draw.js'), 'utf8');
const doodlesJs = readFileSync(join(ROOT, 'templates', 'doodles.js'), 'utf8');
const roughSrc = readFileSync(join(ROOT, 'scripts', 'node_modules', 'roughjs', 'bundled', 'rough.js'), 'utf8');
const theme = flag('--dark') ? 'dark' : flag('--light') ? 'light' : (layout.canvas?.theme || 'dark');
const inkColor = theme === 'dark' ? '#F7F7FC' : '#5F5F73';
const logoFile = theme === 'dark' ? 'arize-logo-pink-white.svg' : 'arize-logo-pink-black.svg';
const arizeLogo = readFileSync(join(ROOT, 'assets', 'brand', logoFile), 'utf8')
  .replace(/<\?xml[^>]*\?>/, '').trim();

// ---------- light validation (budgets) ----------
function warn(m) { console.warn('  ⚠ ' + m); }
if (!layout.sections?.length) { console.error('layout has no sections'); process.exit(1); }
if (layout.sections.length > 12) warn(`${layout.sections.length} sections (>12) — grid will be crowded`);
layout.sections.forEach((s, i) => {
  if ((s.bullets || []).length > 4) warn(`section ${i + 1} "${s.header}" has ${s.bullets.length} bullets (>4)`);
  if ((s.header || '').length > 38) warn(`section ${i + 1} header is long (${s.header.length} chars)`);
});

// ---------- icon (roughen-filtered lucide) ----------
function iconSvg(name, hue) {
  if (!name) return '';
  try {
    const raw = readFileSync(join(ROOT, 'scripts', 'node_modules', 'lucide-static', 'icons', `${name}.svg`), 'utf8');
    const inner = raw.replace(/<!--[\s\S]*?-->/g, '').replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '');
    return `<svg viewBox="0 0 24 24" fill="none" stroke="${hue}" stroke-width="2.1"
      stroke-linecap="round" stroke-linejoin="round" style="filter:url(#roughen)">${inner}</svg>`;
  } catch {
    warn(`icon "${name}" not found in lucide-static — skipping`);
    return '';
  }
}

// inner markup of a lucide icon (for topic-relevant marginalia motifs)
function lucideInner(name) {
  try {
    const raw = readFileSync(join(ROOT, 'scripts', 'node_modules', 'lucide-static', 'icons', `${name}.svg`), 'utf8');
    return raw.replace(/<!--[\s\S]*?-->/g, '').replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '').trim();
  } catch { warn(`motif icon "${name}" not found — skipping`); return null; }
}
const motifSvgs = {};
for (const n of (layout.decor?.motifs || [])) { const inner = lucideInner(n); if (inner) motifSvgs[n] = inner; }

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// ---------- markup ----------
// inner content of a grid cell (banner + figure/icon + bullets + optional quote)
function sectionInner(s, i, compact) {
  const hueName = s.hue || HUE_CYCLE[i % HUE_CYCLE.length];
  const hue = HUES[hueName] || HUES.teal;
  const num = s.n ?? i + 1;
  const blist = compact ? (s.bullets || []).slice(0, 2) : (s.bullets || []);
  const bullets = blist.map((b) => `<li><span class="check"></span>${esc(b)}</li>`).join('');
  const quote = (!compact && s.quote)
    ? `<div class="quote"><svg class="quote-bg"></svg><span class="quote-text">“${esc(s.quote)}”</span></div>` : '';
  let visual;
  if (s.figure) {
    try { visual = `<img class="figure" src="data:image/png;base64,${readFileSync(resolve(ROOT, s.figure)).toString('base64')}"/>`; }
    catch { warn('figure not found: ' + s.figure); visual = `<div class="icon">${iconSvg(s.icon, hue)}</div>`; }
  } else {
    visual = `<div class="icon">${iconSvg(s.icon, hue)}</div>`;
  }
  return `<svg class="cell-bg"></svg>
    <div class="cell-inner">
      <div class="banner" data-hue="${hueName}"><svg class="banner-bg"></svg>
        <span class="num">${num}</span><span class="banner-text">${esc(s.header)}</span></div>
      <div class="cell-body">${visual}<ul class="bullets">${bullets}</ul></div>
      ${quote}
    </div>`;
}
const dataAttrs = (s) => `data-container="${s.container || 'box'}" data-emphasis="${s.emphasis ? 'true' : 'false'}"`;

// grid
const cellsHtml = layout.sections.map((s, i) =>
  `<div class="cell" ${dataAttrs(s)}>${sectionInner(s, i, false)}</div>`).join('\n');

// ---- chrome shared by every layout ----
const speakersHtml = (layout.speakers && layout.speakers.length)
  ? `<div class="speakers">` + layout.speakers.map((sp) => {
      let src = '';
      try { src = 'data:image/png;base64,' + readFileSync(resolve(ROOT, sp.portrait)).toString('base64'); }
      catch { warn('portrait not found: ' + sp.portrait); }
      return `<div class="speaker">${src ? `<span class="portrait-wrap"><img class="portrait" src="${src}"/></span>` : ''}
        <div class="sp-name">${esc(sp.name)}</div><div class="sp-role">${esc(sp.role || '')}</div></div>`;
    }).join('') + `</div>`
  : '';
const topbarHtml = `<div class="topbar">
    <div class="title-block">
      <div class="title">${esc(layout.title)}<span class="title-underline"></span></div>
      ${layout.subtitle ? `<div class="subtitle">${esc(layout.subtitle)}</div>` : ''}
    </div>
    ${speakersHtml}
  </div>`;
const footerHtml = `<div class="footer"><span class="f-logo">${arizeLogo}</span></div>`;

// ---- grid body (fixed 16:9 canvas: 1920×1080 CSS px → 3840×2160 at 2× scale) ----
const N = layout.sections.length;
const C = layout.canvas?.cols || (N <= 6 ? 3 : 4);
const bodyInner = `<div class="grid" style="grid-template-columns:repeat(${C},1fr);grid-auto-rows:1fr">${cellsHtml}</div>`;
const bodyHtml = `${topbarHtml}\n${bodyInner}\n${footerHtml}`;

const canvasHtml = `<div id="canvas" data-theme="${theme}" data-layout="grid">
  <svg width="0" height="0" style="position:absolute"><defs>
    <filter id="roughen"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.4" xChannelSelector="R" yChannelSelector="G"/></filter>
  </defs></svg>
  <svg class="decor-layer" id="decor"></svg>
  ${bodyHtml}
</div>`;

const html = `<!doctype html><html><head><meta charset="utf-8">
<style>${css}</style></head><body style="margin:0;background:#fff">
${canvasHtml}
<script>window.__HUES=${JSON.stringify(HUES)};window.__ACCENT=${JSON.stringify(ACCENT)};window.__INK=${JSON.stringify(inkColor)};
window.__SEED=${Number(opt('--seed', (layout.decor?.seed ?? 7)))};window.__DECOR=${JSON.stringify(opt('--decor', layout.decor?.density || 'light'))};
window.__MOTIFS=${JSON.stringify(motifSvgs)};</script>
<script>${roughSrc}</script>
<script>${doodlesJs}</script>
<script>${drawJs}</script>
</body></html>`;

if (keepHtml) writeFileSync(outBase + '.html', html);

// ---------- render ----------
const browser = await chromium.launch();
const ctx = await browser.newContext({ deviceScaleFactor: scale });
const page = await ctx.newPage();
await page.setContent(html, { waitUntil: 'networkidle' });
await page.evaluate(() => window.__renderSketchnote());
await page.waitForFunction(() => window.__done === true, { timeout: 15000 });

const el = page.locator('#canvas');
await el.screenshot({ path: outBase + '.png' });
console.log('✓ wrote ' + outBase + '.png');

if (emitSvg) {
  const dims = await el.evaluate((n) => ({ w: n.offsetWidth, h: n.offsetHeight }));
  const inner = await el.evaluate((n) => n.outerHTML);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml"
  width="${dims.w}" height="${dims.h}" viewBox="0 0 ${dims.w} ${dims.h}">
  <foreignObject width="${dims.w}" height="${dims.h}">
    <div xmlns="http://www.w3.org/1999/xhtml"><style>${css}</style>${inner}</div>
  </foreignObject>
</svg>`;
  writeFileSync(outBase + '.svg', svg);
  console.log('✓ wrote ' + outBase + '.svg');
}

await browser.close();
