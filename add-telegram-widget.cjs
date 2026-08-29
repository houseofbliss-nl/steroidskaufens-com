// Remplace l'ancien widget statique par un BOUTON FLOTTANT Telegram (@steroidskaufen).
// - Bouton rond bleu (logo Telegram uniquement, AUCUN texte), position:fixed bord gauche.
// - Visible de n'importe où sur la page (ne nécessite pas de scroller).
// - Idempotent : retire l'ancien bloc tg-widget-wrap (si présent) + n'injecte pas 2×.
// Usage : node add-telegram-widget.cjs   (depuis la racine du repo)
const fs = require('fs');
const path = require('path');

// ── bouton flottant (auto-suffisant : <style> + <a>) ──
const FLOAT = `
<!-- tg-float-btn-widget -->
<style>
.tg-float-btn{position:fixed;left:18px;bottom:22px;z-index:99999;width:58px;height:58px;border-radius:50%;background:#229ED9;box-shadow:0 6px 18px rgba(0,0,0,.28),0 3px 10px rgba(34,158,217,.5);display:flex;align-items:center;justify-content:center;text-decoration:none;transition:transform .2s ease,box-shadow .2s ease}
.tg-float-btn:hover{transform:translateY(-2px) scale(1.06);box-shadow:0 10px 24px rgba(0,0,0,.34),0 6px 16px rgba(34,158,217,.55)}
.tg-float-btn::after{content:"";position:absolute;top:-6px;left:-6px;right:-6px;bottom:-6px;border-radius:50%;border:2px solid rgba(34,158,217,.55);opacity:0;animation:tgFloatPulse 2.4s ease-out infinite}
@keyframes tgFloatPulse{0%{transform:scale(.92);opacity:.8}100%{transform:scale(1.32);opacity:0}}
.tg-float-btn svg{display:block}
@media (max-width:560px){.tg-float-btn{left:12px;bottom:14px;width:52px;height:52px}}
@media (prefers-reduced-motion:reduce){.tg-float-btn::after{animation:none}}
</style>
<a class="tg-float-btn" href="https://t.me/steroidskaufen" target="_blank" rel="noopener" aria-label="Telegram @steroidskaufen" title="Telegram @steroidskaufen">
  <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.42z" fill="#fff"/></svg>
</a>
`;

const OLD_START = '<style>\n.tg-widget-wrap{';
const OLD_CTA = 'class="tg-widget-cta"';
const OLD_END = '  </div>\n</div>\n';
const FLOAT_MARK = 'tg-float-btn';

function walk(dir) {
  let out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === '.git') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out = out.concat(walk(p));
    else if (e.name.toLowerCase().endsWith('.html')) out.push(p);
  }
  return out;
}

// retire l'ancien bloc statique s'il existe
function removeOld(s) {
  let out = 0;
  while (true) {
    const w = s.indexOf('<style>\n.tg-widget-wrap{');
    if (w === -1) break;
    const cta = s.indexOf(OLD_CTA, w);
    if (cta === -1) break; // anomalie, ne pas tronquer
    const eStart = s.indexOf(OLD_END, cta);
    if (eStart === -1) break;
    s = s.slice(0, w) + s.slice(eStart + OLD_END.length);
    out++;
  }
  return { s, out };
}

const files = walk(__dirname);
let injected = 0, removedOld = 0, skippedNoBody = 0, skippedAlready = 0;

for (const f of files) {
  let s = fs.readFileSync(f, 'utf8');
  if (s.includes(FLOAT_MARK)) { skippedAlready++; continue; } // déjà le flottant
  let s2 = s;
  const rem = removeOld(s2);
  s2 = rem.s; removedOld += rem.out;
  const i = s2.lastIndexOf('</body>');
  if (i === -1) { skippedNoBody++; continue; }
  const fixed = s2.slice(0, i) + FLOAT + '\n' + s2.slice(i);
  fs.writeFileSync(f, fixed);
  injected++;
}

console.log(JSON.stringify({ total: files.length, injected, removedOld, skippedAlready, skippedNoBody }));