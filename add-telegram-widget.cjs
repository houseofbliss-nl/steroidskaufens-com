// Ajoute un widget Telegram (@steroidskaufen) juste au-dessus du footer sur toutes les pages HTML.
// Idempotent : ne réinjecte pas si le marqueur tg-widget-wrap est déjà présent.
// Usage : node add-telegram-widget.cjs   (depuis la racine du repo)
const fs = require('fs');
const path = require('path');

// ── contenu du widget (auto-suffisant : <style> + markup, couleurs du thème) ──
const WIDGET = `
<style>
.tg-widget-wrap{display:flex;justify-content:center;padding:52px 16px 8px}
.tg-widget{background:#1a1a2e;border:1px solid rgba(39,174,96,.5);border-radius:16px;max-width:740px;width:100%;padding:28px 30px;display:flex;align-items:center;gap:20px;box-shadow:0 14px 36px rgba(0,0,0,.16)}
.tg-widget-icon{flex:0 0 auto;display:flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:#229ED9;box-shadow:0 4px 14px rgba(34,158,217,.45)}
.tg-widget-icon svg{display:block}
.tg-widget-body{flex:1;min-width:0}
.tg-widget-title{margin:0 0 4px;font-size:20px;line-height:1.25;font-weight:800;color:#ffffff}
.tg-widget-text{margin:0;font-size:14px;line-height:1.6;color:rgba(255,255,255,.74)}
.tg-widget-text b{color:#27ae60;font-weight:700}
.tg-widget-cta{flex:0 0 auto;display:inline-flex;align-items:center;gap:9px;background:#27ae60;color:#fff;text-decoration:none;font-weight:800;font-size:14.5px;line-height:1;padding:15px 24px;border-radius:10px;white-space:nowrap;transition:background .18s ease,transform .18s ease}
.tg-widget-cta:hover{background:#239a55;color:#fff;transform:translateY(-1px)}
@media (max-width:560px){.tg-widget-wrap{padding:40px 12px 6px}.tg-widget{flex-direction:column;text-align:center;padding:26px 20px;gap:14px}.tg-widget-cta{margin-top:4px}}
</style>
<div class="tg-widget-wrap">
  <div class="tg-widget">
    <div class="tg-widget-icon" aria-hidden="true">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.42z" fill="#fff"/></svg>
    </div>
    <div class="tg-widget-body">
      <p class="tg-widget-title">Fragen? Schreib uns direkt auf Telegram</p>
      <p class="tg-widget-text">Schnelle Antwort, Beratung &amp; Bestellung direkt im Chat.<br>Unser offizieller Kanal: <b>@steroidskaufen</b></p>
    </div>
    <a class="tg-widget-cta" href="https://t.me/steroidskaufen" target="_blank" rel="noopener">Telegram öffnen</a>
  </div>
</div>
`;

const MARKER = 'tg-widget-wrap';
const ANCHOR = '<footer id="footer">';

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

const files = walk(__dirname);
let injected = 0, skippedNoAnchor = 0, skippedAlready = 0;

for (const f of files) {
  let s = fs.readFileSync(f, 'utf8');
  if (s.includes(MARKER)) { skippedAlready++; continue; }
  const idx = s.indexOf(ANCHOR);
  if (idx === -1) { skippedNoAnchor++; continue; }
  s = s.slice(0, idx) + WIDGET + s.slice(idx);
  fs.writeFileSync(f, s);
  injected++;
}

console.log(JSON.stringify({ total: files.length, injected, skippedAlready, skippedNoAnchor }));

// Page spéciale sans <footer id="footer"> : la confirmation de commande (design custom).
const special = path.join(__dirname, 'de', 'bestellbestatigung.html');
if (fs.existsSync(special)) {
  let s = fs.readFileSync(special, 'utf8');
  if (!s.includes(MARKER)) {
    const i = s.lastIndexOf('</body>');
    if (i === -1) throw new Error('bestellbestatigung.html: pas de </body>');
    s = s.slice(0, i) + WIDGET + '\n' + s.slice(i);
    fs.writeFileSync(special, s);
    console.log(JSON.stringify({ special: 'bestellbestatigung.html', injected: true }));
  }
}
