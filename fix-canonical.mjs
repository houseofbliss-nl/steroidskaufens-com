/**
 * fix-canonical.mjs — Répare les causes GSC identifiées sur /de/
 *
 * 1. DOUBLE CANONICAL : chaque page doit avoir EXACTEMENT une canonical.
 *    On retire TOUTES les <link rel="canonical"> (quel que soit leur forme
 *    PrestaShop : relative href="x.html", href avant rel, ou malformée
 *    "rel=canonical x.html/>" sans href → les 141 doublons résiduels) puis on
 *    ré-injecte l'unique canonical absolue extension-less (calculée depuis le
 *    chemin, identique à seo-enrich.mjs). Idempotent.
 * 2. HREFLANG : on retire tout <link rel="alternate"> qui n'est pas la de-DE
 *    absolue extension-less injectée (relatives .html, x-default, es/nl mortes).
 * 3. ROBOTS :
 *    - /de/content/* : retire le noindex hérité (pages d'info indexables)
 *    - warenkorb.html / warenkorb-original.html : ajoute noindex (panier)
 *    - captures 404 HTTrack (index<hex>.html : page "Fehler 404" servie 200)
 *      → noindex + exclusion du sitemap (sinon soft-404 GSC)
 * 4. SUPPRIME les réponses 404 gzip servies comme .html (nandrolone-*)
 *
 * Usage : node fix-canonical.mjs
 */
import { readdirSync, readFileSync, writeFileSync, unlinkSync } from 'fs';
import { join, dirname, relative } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DE_DIR = join(__dirname, 'de');
const BASE = 'https://steroidskaufen.dealsnows.com';

const stats = {
  pagesAnalysees: 0,
  fichiersModifies: 0,
  canonicalForces: 0,
  alternatesRetires: 0,
  noindexAjoutesPanier: 0,
  noindexRetiresContent: 0,
  noindexAjoutes404: 0,
  gzipSupprimes: 0,
  gzip: [],
};

function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const fp = join(dir, e.name);
    if (e.isDirectory()) { walk(fp); continue; }
    if (!e.name.endsWith('.html')) continue;
    processFile(fp);
  }
}

// Même calcul que seo-enrich.mjs (canonicalUrl) : URL absolue extension-less.
function canonicalFor(relPath) {
  if (/\/?index\.html$/.test(relPath)) {
    const dirn = relPath.replace(/\/?index\.html$/, '');
    return BASE + '/de/' + (dirn ? dirn + '/' : '');
  }
  return BASE + '/de/' + relPath.replace(/\.html$/, '');
}

function processFile(fp) {
  // 4. gzip (réponses 404 HTTrack non décompressées) → suppression (URL 301
  //    vers la vraie page catégorie cf. _redirects, puis 200).
  const buf = readFileSync(fp);
  if (buf.length >= 2 && buf[0] === 0x1f && buf[1] === 0x8b) {
    stats.gzipSupprimes++;
    stats.gzip.push(fp);
    return;
  }

  const html = buf.toString('utf8');
  if (!/<!doctype html|<html/i.test(html) || !/<\/head>/i.test(html)) return; // non-page (AJAX…)
  stats.pagesAnalysees++;

  const rel = relative(DE_DIR, fp).replace(/\\/g, '/');
  let out = html;
  let changed = false;

  // 1. Canonique : forcer EXACTEMENT une seule.
  const desired = canonicalFor(rel);
  // On retire toute balise <link rel="canonical"> (toutes formes/ordres).
  const canonRe = /<link\b[^>]*?rel\s*=\s*"canonical"[^>]*>/gi;
  const canonBefore = out.match(canonRe) || [];
  out = out.replace(canonRe, '');
  if (canonBefore.length) changed = true;
  if (!out.includes(`rel="canonical" href="${desired}"`)) {
    // Ré-injecter l'unique canonique juste après <head>
    out = out.replace(/<head[^>]*>/i, (m) => `${m}\n  <link rel="canonical" href="${desired}">`);
    stats.canonicalForces++;
    changed = true;
  }

  // 2. Alternates : ne garder que la de-DE absolue extension-less (les autres
  //    — relatives .html, x-default, es/, nl/ → 404 — sont retirées).
  out = out.replace(/<link\b[^>]*?rel\s*=\s*"alternate"[^>]*>/gi, (m) => {
    const keep = /hreflang\s*=\s*"de-DE"/.test(m) && m.includes(BASE + '/') && !m.includes('.html');
    if (keep) return m;
    stats.alternatesRetires++;
    changed = true;
    return '';
  });
  if (!/<link\b[^>]*?rel\s*=\s*"alternate"[^>]*hreflang\s*=\s*"de-DE"/i.test(out)) {
    out = out.replace(/<head[^>]*>/i, (m) => `${m}\n  <link rel="alternate" hreflang="de-DE" href="${desired}">`);
    changed = true;
  }

  const isContentTrust = /^content\//.test(rel);          // pages d'info → indexable
  const isCart = /warenkorb(?:-|\.html|$)/.test(fp);      // panier → noindex
  const is404Snapshot = /index[0-9a-f]{4,}\.html$/.test(fp); // captures 404 HTTrack

  const hasRobots = /<meta\s+name="robots"/i.test(out);

  // 3a. Content → noindex hérité retiré
  if (isContentTrust) {
    const before = out;
    out = out.replace(/<meta\s+name="robots"\s+content="[^"]*"[^>]*>/gi, (m) => {
      stats.noindexRetiresContent++;
      changed = true;
      return '';
    });
  }

  // 3b. Cart et 404-snapshots → noindex si absent
  if ((isCart || is404Snapshot) && !hasRobots) {
    out = out.replace(/<head>/i, '<head>\n  <meta name="robots" content="noindex,nofollow">');
    if (isCart) stats.noindexAjoutesPanier++;
    if (is404Snapshot) stats.noindexAjoutes404++;
    changed = true;
  }

  if (changed) {
    try { writeFileSync(fp, out, 'utf8'); } catch {}
    stats.fichiersModifies++;
  }
}

walk(DE_DIR);

for (const fp of stats.gzip) {
  try { unlinkSync(fp); } catch {}
}

console.log('=== fix-canonical.mjs — résumé ===');
console.log(JSON.stringify(
  {
    pagesAnalysees: stats.pagesAnalysees,
    fichiersModifies: stats.fichiersModifies,
    canonicalForces: stats.canonicalForces,
    alternatesRetires: stats.alternatesRetires,
    noindexAjoutesPanier: stats.noindexAjoutesPanier,
    noindexRetiresContent: stats.noindexRetiresContent,
    noindexAjoutes404: stats.noindexAjoutes404,
    gzipSupprimes: stats.gzipSupprimes,
    fichiersGzip: stats.gzip.map((f) => f.replace(DE_DIR + '\\', '').replace(/\\/g, '/')),
  },
  null,
  2
));