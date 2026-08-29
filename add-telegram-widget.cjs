// BOUTON FLOTTANT Telegram (@steroidskaufen) — rond bleu logo, position:fixed à DROITE,
// remonté entre le bouton TOP (.scrollTop, right:25px bottom:90px) et le bloc Avis
// (onglet Judge.me, bord droit centre vertical). AUCUN effet de vague.
// "Upsert" : remplace la version tg-float-btn existante OU insère avant </body>.
// Usage : node add-telegram-widget.cjs   (depuis la racine du repo)
const fs = require('fs');
const path = require('path');

const MARKER = '<!-- tg-float-btn-widget -->';
// Message d'ouverture pré-rempli (allemand) quand le client clique sur le bouton.
const TG_MSG = encodeURIComponent(
  'Hallo! Ich möchte gerne eine Bestellung auf Steroidskaufen aufgeben. Könnt ihr mir dabei helfen?'
);
const TG_URL = `https://t.me/steroidskaufen?text=${TG_MSG}`;

const FLOAT = MARKER + `
<style>
.tg-float-btn{position:fixed;right:25px;bottom:24%;z-index:99999;width:58px;height:58px;border-radius:50%;background:#229ED9;box-shadow:0 6px 18px rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center;text-decoration:none;transition:transform .15s ease}
.tg-float-btn:hover{transform:scale(1.05)}
.tg-float-btn svg{display:block}
@media (max-width:560px){.tg-float-btn{right:12px;bottom:24%;width:52px;height:52px}}
</style>
<a class="tg-float-btn" href="${TG_URL}" target="_blank" rel="noopener" aria-label="Telegram @steroidskaufen" title="Telegram @steroidskaufen">
  <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.42z" fill="#fff"/></svg>
</a>
`;

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
let upserted = 0, inserted = 0, skippedNoBody = 0;
const POST_open = '</a>\n';

for (const f of files) {
  let s = fs.readFileSync(f, 'utf8');
  const start = s.indexOf(MARKER);
  if (start !== -1) {
    // remplace l'ancienne version (de la balise commentaire jusqu'au </a> fermant)
    const aEnd = s.indexOf('</a>', start);
    if (aEnd === -1 || aEnd < start) { skippedNoBody++; continue; }
    const end = aEnd + POST_open.length;
    s = s.slice(0, start) + FLOAT + s.slice(end);
    fs.writeFileSync(f, s);
    upserted++;
    continue;
  }
  const i = s.lastIndexOf('</body>');
  if (i === -1) { skippedNoBody++; continue; }
  s = s.slice(0, i) + FLOAT + '\n' + s.slice(i);
  fs.writeFileSync(f, s);
  inserted++;
}

console.log(JSON.stringify({ total: files.length, upserted, inserted, skippedNoBody }));
