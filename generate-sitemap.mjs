/**
 * generate-sitemap.mjs — Génère public/sitemap.xml avec toutes les URLs
 * extension-less (style Cloudflare clean URLs / PrestaShop), + dernières
 * modifs (mtime du fichier source) + priorité 1.0 pour la home.
 *
 * Usage : node generate-sitemap.mjs   →   write public/sitemap.xml
 */
import { readFileSync, readdirSync, writeFileSync, statSync, mkdirSync, existsSync } from 'fs';
import { join, dirname, relative } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DE_DIR = join(__dirname, 'de');
const OUT_DIR = join(__dirname, 'public');
const OUT_FILE = join(OUT_DIR, 'sitemap.xml');
const BASE = 'https://steroidskaufen.dealsnows.com';

// Fichiers à exclure : non-HTML (gzip 404, AJAX JSON…) — même garde que seo-enrich.mjs
// + pages noindex (paniers warenkorb*) : elles ne doivent pas être soumises au
// sitemap (une URL soumise + noindex = "Exclue par la balise noindex" dans GSC).
function isRealPage(fp) {
  if (!fp.endsWith('.html')) return false;
  let h;
  try { h = readFileSync(fp, 'utf8'); } catch { return false; }
  if (!/<!doctype html|<html/i.test(h) || !/<\/head>/i.test(h)) return false;
  if (/<meta\s+name="robots"\s+content="[^"]*noindex/i.test(h)) return false;
  return true;
}

// Duplicats HTTrack (variantes d'URL à suffixe hexadécimal, ex. 10-orale-steroide4658.html) :
// contenu identique à la page sans suffixe → à ne PAS soumettre au sitemap
// (sinon Google les traite comme des pages distinctes auto-canonical = "page en
// double sans canonical"). Détection : le fichier sans le suffixe hex existe déjà.
const isHashDuplicate = (dir, rel, nameNoExt) => {
  const m = /([0-9a-fA-F]{4,})$/.exec(nameNoExt);
  if (!m) return false;
  const base = nameNoExt.slice(0, nameNoExt.length - m[1].length) + '.html';
  // Duplicat UNIQUEMENT si une vraie page sans ce suffixe existe à côté.
  return existsSync(join(dir, base));
};

const files = [];
function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const fp = join(dir, e.name);
    if (e.isDirectory()) { walk(fp); continue; }
    if (!isRealPage(fp)) continue;
    const rel = relative(DE_DIR, fp).replace(/\\/g, '/');
    if (isHashDuplicate(dir, rel, e.name.replace(/\.html$/, ''))) continue;
    const lastmod = statSync(fp).mtime.toISOString().split('T')[0];
    let url;
    if (/\/?index\.html$/.test(rel)) {
      const dir2 = rel.replace(/\/?index\.html$/, '');
      url = BASE + '/de/' + (dir2 ? dir2 + '/' : '');
    } else {
      url = BASE + '/de/' + rel.replace(/\.html$/, '');
    }
    files.push({ url, lastmod });
  }
}
walk(DE_DIR);

files.sort((a, b) => a.url.localeCompare(b.url));
// Home en tête avec priorité 1.0
files.sort((a, b) => {
  const aHome = a.url === BASE + '/de/';
  const bHome = b.url === BASE + '/de/';
  if (aHome !== bHome) return aHome ? -1 : 1;
  return a.url.localeCompare(b.url);
});
files.forEach((f, i) => { f.priority = i === 0 ? '1.0' : '0.8'; });

const xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
  + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
  + files.map(f => `  <url>\n    <loc>${f.url}</loc>\n    <lastmod>${f.lastmod}</lastmod>\n    <priority>${f.priority}</priority>\n  </url>`).join('\n')
  + '\n</urlset>\n';

mkdirSync(OUT_DIR, { recursive: true });
writeFileSync(OUT_FILE, xml, 'utf8');
// Copie à la racine : le root de Cloudflare Pages = racine du repo (le site
// entier vit à la racine, pas dans public/), donc /sitemap.xml doit être ici.
writeFileSync(join(__dirname, 'sitemap.xml'), xml, 'utf8');
console.log(`Sitemap écrit : ${OUT_FILE} + racine/sitemap.xml`);
console.log(`URLs : ${files.length}`);