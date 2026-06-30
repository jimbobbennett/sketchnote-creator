/* Procedural hand-drawn marginalia + container shapes, drawn with rough.js.
   Runs in the page; exposes window.Doodles. All functions append SVG nodes to a
   target <svg> whose coordinate space matches where you want to draw. Colors come
   from the caller (the design system's palette). Everything is deterministic given the caller's seed. */
(function () {
  const R = () => window.rough;

  // 5-point star
  function starPoints(cx, cy, r, inner) {
    const pts = [];
    for (let i = 0; i < 10; i++) {
      const ang = (Math.PI / 5) * i - Math.PI / 2;
      const rad = i % 2 ? r * inner : r;
      pts.push([cx + Math.cos(ang) * rad, cy + Math.sin(ang) * rad]);
    }
    return pts;
  }

  window.Doodles = {
    // a 4-point twinkle/sparkle (filled)
    sparkle(svg, cx, cy, s, color) {
      const rc = R().svg(svg);
      const k = s * 0.28;
      const pts = [[cx, cy - s], [cx + k, cy - k], [cx + s, cy], [cx + k, cy + k],
                   [cx, cy + s], [cx - k, cy + k], [cx - s, cy], [cx - k, cy - k]];
      svg.appendChild(rc.polygon(pts, { fill: color, fillStyle: 'solid', stroke: color, strokeWidth: 1, roughness: 1.1 }));
    },
    // 5-point star (outline)
    star(svg, cx, cy, s, color) {
      const rc = R().svg(svg);
      svg.appendChild(rc.polygon(starPoints(cx, cy, s, 0.42), { stroke: color, strokeWidth: 1.6, roughness: 1.3 }));
    },
    // emphasis starburst (many spikes) — good behind a number or "!" moment
    burst(svg, cx, cy, s, color) {
      const rc = R().svg(svg);
      const pts = [];
      const spikes = 11;
      for (let i = 0; i < spikes * 2; i++) {
        const ang = (Math.PI / spikes) * i;
        const rad = i % 2 ? s * 0.55 : s;
        pts.push([cx + Math.cos(ang) * rad, cy + Math.sin(ang) * rad]);
      }
      svg.appendChild(rc.polygon(pts, { stroke: color, strokeWidth: 1.4, roughness: 1.4 }));
    },
    // little curved accent arrow from (x1,y1) to (x2,y2)
    arrow(svg, x1, y1, x2, y2, color) {
      const rc = R().svg(svg);
      const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
      const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
      const bow = Math.min(28, len * 0.25);
      const cxp = mx - (dy / len) * bow, cyp = my + (dx / len) * bow;
      svg.appendChild(rc.path(`M ${x1} ${y1} Q ${cxp} ${cyp} ${x2} ${y2}`, { stroke: color, strokeWidth: 2, roughness: 1.4 }));
      const ang = Math.atan2(y2 - cyp, x2 - cxp), h = 9;
      svg.appendChild(rc.line(x2, y2, x2 - h * Math.cos(ang - 0.5), y2 - h * Math.sin(ang - 0.5), { stroke: color, strokeWidth: 2, roughness: 1 }));
      svg.appendChild(rc.line(x2, y2, x2 - h * Math.cos(ang + 0.5), y2 - h * Math.sin(ang + 0.5), { stroke: color, strokeWidth: 2, roughness: 1 }));
    },
    // underline swoosh under a span
    swoosh(svg, x, y, w, color) {
      const rc = R().svg(svg);
      svg.appendChild(rc.path(`M ${x} ${y} Q ${x + w * 0.5} ${y + 7} ${x + w} ${y - 1}`, { stroke: color, strokeWidth: 3, roughness: 1.4 }));
    },
    // curly/curved decorative line
    squiggle(svg, x, y, w, color) {
      const rc = R().svg(svg);
      const seg = w / 3;
      svg.appendChild(rc.path(`M ${x} ${y} q ${seg / 2} -8 ${seg} 0 t ${seg} 0 t ${seg} 0`, { stroke: color, strokeWidth: 1.6, roughness: 1.1 }));
    },
    // dots cluster
    dots(svg, cx, cy, color) {
      const rc = R().svg(svg);
      [[0, 0], [7, 3], [-5, 5]].forEach(([dx, dy]) =>
        svg.appendChild(rc.circle(cx + dx, cy + dy, 3, { fill: color, fillStyle: 'solid', stroke: color, strokeWidth: 0.5, roughness: 0.8 })));
    },

    // ---- containers (drawn into a per-element overlay svg sized w×h) ----
    // rounded box
    box(svg, w, h, color, opts = {}) {
      const rc = R().svg(svg);
      svg.appendChild(rc.rectangle(4, 4, w - 8, h - 8, { stroke: color, strokeWidth: opts.sw || 2.4, roughness: 1.9, bowing: 1.1 }));
    },
    // speech bubble with a tail at bottom-left
    speechBubble(svg, w, h, color, opts = {}) {
      const rc = R().svg(svg);
      const r = 14, bh = h - 14; // leave room for tail
      const d = `M ${4 + r} 4 L ${w - 4 - r} 4 Q ${w - 4} 4 ${w - 4} ${4 + r}
                 L ${w - 4} ${bh - r} Q ${w - 4} ${bh} ${w - 4 - r} ${bh}
                 L ${36} ${bh} L ${22} ${h - 4} L ${24} ${bh} L ${4 + r} ${bh}
                 Q 4 ${bh} 4 ${bh - r} L 4 ${4 + r} Q 4 4 ${4 + r} 4 Z`;
      svg.appendChild(rc.path(d, { stroke: color, strokeWidth: opts.sw || 2.2, roughness: 1.1, bowing: 0.8 }));
    },
    // cloud container — scalloped blob (used for keystone / "soft idea" cells)
    cloud(svg, w, h, color, opts = {}) {
      const rc = R().svg(svg);
      const pad = 8, by = h - pad, ty = pad + 12;
      const bumps = Math.max(3, Math.round(w / 95));
      const step = (w - 2 * pad) / bumps;
      let d = `M ${pad} ${by}`;
      d += ` Q ${pad - 9} ${(by + ty) / 2} ${pad} ${ty}`;            // left side bump
      for (let i = 0; i < bumps; i++) {                               // top scallops
        const x0 = pad + i * step;
        d += ` Q ${x0 + step / 2} ${ty - 18} ${x0 + step} ${ty}`;
      }
      d += ` Q ${w - pad + 9} ${(by + ty) / 2} ${w - pad} ${by}`;     // right side bump
      for (let i = bumps; i > 0; i--) {                               // gentle bottom scallops
        const x0 = pad + i * step;
        d += ` Q ${x0 - step / 2} ${by + 7} ${x0 - step} ${by}`;
      }
      d += ' Z';
      svg.appendChild(rc.path(d, { stroke: color, strokeWidth: opts.sw || 2.3, roughness: 1.6, bowing: 1 }));
    },
    // highlight wash — translucent hachure fill behind something (no stroke)
    wash(svg, x, y, w, h, color) {
      const rc = R().svg(svg);
      const g = rc.rectangle(x, y, w, h, { fill: color, fillStyle: 'hachure', hachureGap: 5, fillWeight: 2.2, stroke: 'none', roughness: 1.6 });
      g.setAttribute('opacity', '0.22');
      svg.appendChild(g);
    },
  };
})();
