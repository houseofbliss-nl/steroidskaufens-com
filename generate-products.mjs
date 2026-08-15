/**
 * generate-products.mjs — Scannt alle Produktseiten unter de/ und schreibt
 * data/products.json (echte deutsche Namen, Preise, URLs aus den Seiten).
 *
 * Usage : node generate-products.mjs
 * Output : data/products.json
 */
import { readFileSync, readdirSync, writeFileSync } from 'fs';
import { join, dirname, relative } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DE_DIR = join(__dirname, 'de');
const OUTPUT = join(__dirname, 'data', 'products.json');

const products = [];

function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const fp = join(dir, e.name);
    if (e.isDirectory()) walk(fp);
    else if (e.name.endsWith('.html')) scan(fp);
  }
}

function scan(filePath) {
  let html;
  try { html = readFileSync(filePath, 'utf8'); } catch { return; }

  if (!html.includes('itemprop="price"')) return;

  const titleMatch = html.match(/<title>([^<]+)<\/title>/);
  if (!titleMatch) return;
  const title = titleMatch[1].trim();

  const relPath = relative(DE_DIR, filePath).replace(/\\/g, '/');

  let image = '';
  const imgMatch = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/);
  if (imgMatch) {
    image = imgMatch[1].replace(/^https?:\/\/steroidskaufen\.com\//, '/');
  }

  // Nom depuis le H1 produit (prioritaire)
  let name = '';
  const h1Match = html.match(/<h1[^>]*itemprop="name"[^>]*>([^<]+)<\/h1>/)
    || html.match(/<h1[^>]*class="[^"]*h1[^"]*"[^>]*>([^<]+)<\/h1>/);
  if (h1Match) name = h1Match[1].trim();
  if (!name) name = title;

  // Prix principal : bloque .product-prices si possible
  let price = '';
  const contentMatch = html.match(/<span\s+itemprop="price"[^>]*\s+content="([^"]+)"/);
  if (contentMatch) {
    price = contentMatch[1];
  } else {
    const pp = html.match(/<div[^>]*class="[^"]*product-prices[^"]*"[^>]*>([\s\S]*?)<\/div>/);
    if (pp) {
      const ppPrice = pp[1].match(/<span[^>]*itemprop="price"[^>]*>([^<]+)<\/span>/);
      if (ppPrice) price = ppPrice[1].trim().replace(/[^\d,.]/g, '').replace(/\./g, '').replace(',', '.');
    }
  }
  if (!price) return;

  products.push({
    name,                 // ex. "Parabolan"
    price: parseFloat(price),
    url: '/de/' + relPath,  // ex. "/de/fatburner/550-3-x-retatrutide-4mg-pen.html"
    image
  });
}

console.log('Scan des produits…');
walk(DE_DIR);
products.sort((a, b) => a.name.localeCompare(b.name, 'de'));
console.log(`${products.length} produits trouvés`);

writeFileSync(OUTPUT, JSON.stringify(products, null, 2), 'utf8');
console.log(`→ ${OUTPUT}`);