/**
 * build-index.js — Scanne tous les produits et génère product-index.js
 *
 * Usage : node build-index.js
 * Output : assets/js/product-index.js (utilisé par l'autocomplete recherche)
 */
const fs = require('fs');
const path = require('path');

const DE_DIR = path.join(__dirname, 'de');
const OUTPUT = path.join(__dirname, 'assets', 'js', 'product-index.js');

const products = [];

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const fp = path.join(dir, e.name);
    if (e.isDirectory()) walk(fp);
    else if (e.name.endsWith('.html')) scan(fp);
  }
}

function scan(filePath) {
  let html;
  try { html = fs.readFileSync(filePath, 'utf8'); } catch { return; }

  // Must have product price to be a product page
  if (!html.includes('itemprop="price"')) return;

  // Extract title
  const titleMatch = html.match(/<title>([^<]+)<\/title>/);
  if (!titleMatch) return;
  const title = titleMatch[1].trim();

  // Extract relative URL (from filePath to de/ directory)
  const relPath = path.relative(DE_DIR, filePath).replace(/\\/g, '/');

  // Extract image from og:image
  const imgMatch = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/);
  let image = imgMatch ? imgMatch[1] : '';
  // Make image path relative if it's absolute
  if (image.includes('steroidskaufen.com')) {
    image = image.replace(/https?:\/\/steroidskaufen\.com\//, '/');
  }

  // Try JSON-LD for clean data
  const ldMatch = html.match(/<script type="application\/ld\+json">\{[\s\S]*?"@type":"Product"[\s\S]*?\}<\/script>/);
  let price = '';
  let name = '';

  if (ldMatch) {
    try {
      const raw = ldMatch[0]
        .replace(/<script[^>]*>/, '')
        .replace(/<\/script>/, '')
        .replace(/\\"/g, '"')
        .replace(/\\n/g, '')
        .replace(/\\t/g, '')
        .replace(/\\\//g, '/');

      // Extract just the JSON object
      const jsonStart = raw.indexOf('{');
      const jsonEnd = raw.lastIndexOf('}');
      if (jsonStart >= 0 && jsonEnd > jsonStart) {
        const jsonStr = raw.substring(jsonStart, jsonEnd + 1);
        const data = JSON.parse(jsonStr);
        name = data.name || '';
        if (data.offers) {
          price = data.offers.price || '';
        }
      }
    } catch (e) {
      // JSON parse failed, fallback below
    }
  }

  // Fallback: extract name from H1
  if (!name) {
    const h1Match = html.match(/<h1[^>]*itemprop="name"[^>]*>([^<]+)<\/h1>/);
    name = h1Match ? h1Match[1].trim() : title;
  }

  // Fallback: extract price from itemprop with content attribute (main product price)
  if (!price) {
    // First try: itemprop with content="XX" (main product, not suggested)
    const contentMatch = html.match(/<span\s+itemprop="price"[^>]*\s+content="([^"]+)"/);
    if (contentMatch) {
      price = contentMatch[1];
    } else {
      // Second try: the price inside <div class="product-prices">
      const ppSection = html.match(/<div[^>]*class="[^"]*product-prices[^"]*"[^>]*>([\s\S]*?)<\/div>/);
      if (ppSection) {
        const ppPrice = ppSection[1].match(/<span[^>]*itemprop="price"[^>]*>([^<]+)<\/span>/);
        if (ppPrice) {
          price = ppPrice[1].trim().replace(/[^\d,.]/g, '').replace(/\./g, '').replace(',', '.');
        }
      }
    }
  }

  if (!name) return;

  // Only keep entries with a valid price (real product pages)
  if (!price) return;

  products.push({
    n: name,          // product name
    p: price,         // price
    u: relPath,       // URL relative to de/
    i: image,         // image URL
    t: title          // page title
  });
}

console.log('Scanning product pages...');
walk(DE_DIR);
console.log(`Found ${products.length} products.`);

// Sort alphabetically
products.sort((a, b) => a.n.localeCompare(b.n));

// Generate JS
const js = `/**
 * product-index.js — Index des produits pour la recherche autocomplete
 * Généré automatiquement par build-index.js
 * ${new Date().toISOString().split('T')[0]} — ${products.length} produits
 */
window.productIndex = ${JSON.stringify(products, null, 0)};
`;

fs.writeFileSync(OUTPUT, js, 'utf8');
console.log(`Index written to ${OUTPUT}`);
