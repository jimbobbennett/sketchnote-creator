/* Runs in the page. Uses global `rough` + window.Doodles to draw the hand-drawn layer:
   containers (box / cloud / speech-bubble), hue banners, bullet checks, quote bubbles,
   title underline, and a seeded marginalia decoration pass. Sets window.__done when finished. */
window.__renderSketchnote = async function () {
  await document.fonts.ready;
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));

  const HUES = window.__HUES;
  const ACCENT = window.__ACCENT;
  const INK = window.__INK;
  const D = window.Doodles;
  const canvasEl = document.getElementById('canvas');

  const fit = (svg, el) => {
    const r = el.getBoundingClientRect();
    svg.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
    svg.setAttribute('width', r.width);
    svg.setAttribute('height', r.height);
    svg.setAttribute('preserveAspectRatio', 'none');
    return r;
  };
  const rc = (svg) => rough.svg(svg);
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // subtle hand-drawn cell borders — each edge drawn separately with a slightly randomised
  // stroke weight (seeded → deterministic) so the lines read as sketched, not mechanical
  const bRnd = mulberry32((((window.__SEED || 7) * 9 + 5) >>> 0));
  document.querySelectorAll('.cell').forEach((cell) => {
    const bg = cell.querySelector('.cell-bg');
    const r = fit(bg, cell);
    const rcb = rc(bg);
    const x0 = 3, y0 = 3, x1 = r.width - 3, y1 = r.height - 3;
    const edge = (a, b, c, d) => {
      const n = rcb.line(a, b, c, d, { stroke: INK, strokeWidth: 1.15 + bRnd() * 1.05, roughness: 1.7, bowing: 1.2 });
      n.setAttribute('opacity', '0.4');
      bg.appendChild(n);
    };
    edge(x0, y0, x1, y0);   // top
    edge(x1, y0, x1, y1);   // right
    edge(x1, y1, x0, y1);   // bottom
    edge(x0, y1, x0, y0);   // left
  });

  // hue banners (solid fill, knockout text via CSS)
  document.querySelectorAll('.banner').forEach((banner) => {
    const hue = HUES[banner.dataset.hue] || HUES.teal;
    const bg = banner.querySelector('.banner-bg');
    const r = fit(bg, banner);
    bg.appendChild(rc(bg).rectangle(2, 2, r.width - 4, r.height - 4, {
      fill: hue, fillStyle: 'solid', stroke: hue, strokeWidth: 1.4, roughness: 1.0, bowing: 0.6
    }));
  });

  // checkmark bullets (accent)
  document.querySelectorAll('.bullets li .check').forEach((c) => {
    fit(c, c);
    c.appendChild(rc(c).linearPath([[3, 11], [8, 16], [17, 4]], { stroke: ACCENT, strokeWidth: 2.6, roughness: 1.3 }));
  });

  // quotes as speech bubbles (accent)
  document.querySelectorAll('.quote').forEach((q) => {
    const bg = q.querySelector('.quote-bg');
    const r = fit(bg, q);
    D.speechBubble(bg, r.width, r.height, ACCENT, { sw: 1.8 });
  });

  // title underline (accent)
  const tu = document.querySelector('.title-underline');
  if (tu) {
    const r = fit(tu, tu);
    tu.appendChild(rc(tu).linearPath([[2, 9], [r.width * 0.5, 4], [r.width - 2, 10]], { stroke: ACCENT, strokeWidth: 4, roughness: 1.5 }));
  }

  // ---- marginalia decoration pass (seeded, only in free zones) ----
  const decor = document.getElementById('decor');
  const density = window.__DECOR || 'light';
  if (decor && density !== 'none' && D) {
    const cR = canvasEl.getBoundingClientRect();
    fit(decor, canvasEl);
    const obstacles = [...canvasEl.querySelectorAll('.cell, .title, .subtitle, .footer, .speakers')].map((el) => {
      const r = el.getBoundingClientRect();
      return { x: r.left - cR.left, y: r.top - cR.top, w: r.width, h: r.height };
    });
    const free = (x, y, pad) => !obstacles.some((o) => x > o.x - pad && x < o.x + o.w + pad && y > o.y - pad && y < o.y + o.h + pad);
    const rnd = mulberry32((window.__SEED || 7) >>> 0);
    const pick = () => {
      for (let i = 0; i < 80; i++) {
        const x = 12 + rnd() * (cR.width - 24), y = 12 + rnd() * (cR.height - 24);
        if (free(x, y, 16)) return { x, y };
      }
      return null;
    };
    const SVGNS = 'http://www.w3.org/2000/svg';
    const MOTIFS = window.__MOTIFS || {};
    const motifNames = Object.keys(MOTIFS);
    const stampMotif = (name, x, y, size, color) => {
      const inner = MOTIFS[name]; if (!inner) return;
      const s = document.createElementNS(SVGNS, 'svg');
      s.setAttribute('x', x - size / 2); s.setAttribute('y', y - size / 2);
      s.setAttribute('width', size); s.setAttribute('height', size);
      s.setAttribute('viewBox', '0 0 24 24');
      s.setAttribute('fill', 'none'); s.setAttribute('stroke', color);
      s.setAttribute('stroke-width', '2'); s.setAttribute('stroke-linecap', 'round'); s.setAttribute('stroke-linejoin', 'round');
      s.style.filter = 'url(#roughen)';
      s.innerHTML = inner;
      decor.appendChild(s);
    };
    const palette = [ACCENT, HUES.teal, HUES.indigo, HUES.purple];
    const kinds = ['sparkle', 'star', 'dots', 'squiggle', 'sparkle', 'burst'];
    const N = density === 'medium' ? 11 : density === 'heavy' ? 18 : 6;
    for (let i = 0; i < N; i++) {
      const p = pick(); if (!p) continue;
      const c = palette[Math.floor(rnd() * palette.length)];
      // ~55% topic-relevant motif icon (if provided), else a small flourish
      if (motifNames.length && rnd() < 0.55) {
        stampMotif(motifNames[Math.floor(rnd() * motifNames.length)], p.x, p.y, 20 + rnd() * 8, c);
        continue;
      }
      const k = kinds[Math.floor(rnd() * kinds.length)];
      const s = 7 + rnd() * 7;
      if (k === 'sparkle') D.sparkle(decor, p.x, p.y, s, c);
      else if (k === 'star') D.star(decor, p.x, p.y, s, c);
      else if (k === 'burst') D.burst(decor, p.x, p.y, s * 0.9, c);
      else if (k === 'dots') D.dots(decor, p.x, p.y, c);
      else D.squiggle(decor, p.x - s, p.y, s * 2.4, c);
    }
  }

  window.__done = true;
};
