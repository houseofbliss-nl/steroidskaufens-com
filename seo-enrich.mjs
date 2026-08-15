/**
 * seo-enrich.mjs — Injection SEO complète dans les pages HTML de /de/
 *
 * Dans CHAQUE page :
 *   - <script>document.documentElement.classList.add('js')</script>
 *   - <style> html.js .seo-block{display:none} … </style>
 *   - meta geo.region DE / geo.placename Deutschland
 *   - <link rel="canonical"> (URLs extensionless, style PrestaShop)
 *   - <link rel="alternate" hreflang="de-DE">
 *   - JSON-LD OnlineStore (toutes) + Product (pages produit) + FAQPage (home)
 *   - Section visible .seo-city-info + blocs .seo-block (villes, produits, FAQ)
 *
 * Usage : node seo-enrich.mjs            (toutes les pages)
 *         node seo-enrich.mjs --limit 8  (test sur 8 fichiers)
 */
import { readdirSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname, relative } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DE_DIR = join(__dirname, 'de');
const BASE = 'https://steroidskaufen.dealsnows.com';
const MARKER = 'seo-enriched-v1';
const SHOP_NAME = 'Steroidekaufen.com';
const SHOP_LOGO = BASE + '/img/steroide-kaufen-logo-1637164827.jpg';

const cities = JSON.parse(readFileSync(join(__dirname, 'data', 'german-cities.json'), 'utf8'));
const products = JSON.parse(readFileSync(join(__dirname, 'data', 'products.json'), 'utf8'));
const faqs = JSON.parse(readFileSync(join(__dirname, 'data', 'faqs.json'), 'utf8'));
const storeTpl = JSON.parse(readFileSync(join(__dirname, 'templates', 'onlinestore.json'), 'utf8'));

const args = process.argv.slice(2);
const limit = args.includes('--limit') ? parseInt(args[args.indexOf('--limit') + 1], 10) : Infinity;
const POPULAR = products.slice(0, 12);

// ---------- helpers ----------
function canonicalUrl(relPath) {
  if (/\/?index\.html$/.test(relPath)) {
    const dir = relPath.replace(/\/?index\.html$/, '');
    return BASE + '/de/' + (dir ? dir + '/' : '');
  }
  return BASE + '/de/' + relPath.replace(/\.html$/, '');
}
function cleanUrl(u) { return u.replace(/\.html$/, ''); }
function resolveUrl(u, relPath) {
  if (/^https?:\/\//.test(u)) return u.replace(/^https?:\/\/steroidskaufen\.com\//, BASE + '/');
  try { return new URL(u, BASE + '/de/' + relPath).href; } catch { return u; }
}

// ---------- blocs HTML ----------
function seoCityInfo() {
  const names = cities.slice(0, 8).map(c => c.name).join(', ');
  return `<section class="seo-city-info">
    <h2 class="seo-city-info__title">Wir liefern diskret in ganz Deutschland</h2>
    <p class="seo-city-info__text">Bestellen Sie bequem online in unserem Steroide-Shop – diskreter und schneller Versand in alle deutschen Großstädte, unter anderem ${names} und viele weitere Städte in ganz Deutschland.</p>
  </section>`;
}
function seoCityBlock() {
  const lis = cities.map(c => `<li><a href="/de/${c.slug}/">${c.name}</a></li>`).join('\n        ');
  return `<section class="seo-block seo-cities">
    <h2 class="seo-block__title">Städte</h2>
    <ul class="seo-block__list">
        ${lis}
    </ul>
  </section>`;
}
function seoPopularBlock() {
  const lis = POPULAR.map(p => `<li><a href="${cleanUrl(p.url)}">${p.name}</a></li>`).join('\n        ');
  return `<section class="seo-block seo-popular">
    <h2 class="seo-block__title">Beliebte Produkte</h2>
    <ul class="seo-block__list">
        ${lis}
    </ul>
  </section>`;
}
function seoFaqBlock() {
  const items = faqs.map(f => `<dt>${f.question}</dt><dd>${f.answer}</dd>`).join('\n        ');
  return `<section class="seo-block seo-faq">
    <h2 class="seo-block__title">Häufige Fragen</h2>
    <dl class="seo-block__faq">
        ${items}
    </dl>
  </section>`;
}

// ---------- classification / extraction ----------
function pageData(html, relPath) {
  const isHome = /\/?index\.html$/.test(relPath);
  const isProduct = html.includes('class="product-prices"');
  const title = (html.match(/<title>([^<]*)<\/title>/i) || [])[1]?.trim() || '';
  let product = null;
  if (isProduct) {
    const nameMatch = html.match(/<h1[^>]*itemprop="name"[^>]*>([^<]+)<\/h1>/i)
      || html.match(/<h1[^>]*class="h1"[^>]*>([^<]+)<\/h1>/i);
    let price = '';
    // Priorité : attribut content="…" (schéma PrestaShop, ex. <span itemprop="price" content="273">)
    const contentMatch = html.match(/<span[^>]*itemprop="price"[^>]*\s+content="([^"]+)"/i);
    if (contentMatch) {
      price = contentMatch[1];
    } else {
      // Fallback : span itemprop="price" à l'intérieur du bloc .product-prices
      // (on découpe le bloc au <div class="product-discount"> via indexOf, pas en regex
      //  non-greedy qui s'arrêtait au 1er </div> interne → prix vide)
      const blk = html.indexOf('class="product-prices"');
      if (blk !== -1) {
        const seg = html.slice(blk, blk + 3000);
        const pSpan = (seg.match(/<span[^>]*itemprop="price"[^>]*>([^<]+)<\/span>/i) || [])[1];
        if (pSpan) price = pSpan.trim().replace(/[^\d,.]/g, '').replace(/\./g, '').replace(',', '.');
      }
    }
    const og = html.match(/<meta[^>]+property="og:image"[^>]+content="([^"]+)"/i)
      || html.match(/<meta[^>]+content="([^"]+)"[^>]+property="og:image"/i);
    product = {
      name: (nameMatch ? nameMatch[1].trim() : '') || title || SHOP_NAME,
      price: parseFloat(price) || 0,
      image: og ? resolveUrl(og[1], relPath) : SHOP_LOGO
    };
  }
  return { isHome, isProduct, title, product };
}

function storeLd(canonical, image) {
  const copy = JSON.parse(JSON.stringify(storeTpl));
  copy.name = SHOP_NAME;
  copy.url = canonical;
  copy.image = image || SHOP_LOGO;
  copy.priceRange = '€€';
  return copy;
}

// ---------- enrichir un fichier ----------
function enrichFile(fp, relPath) {
  let html = readFileSync(fp, 'utf8');
  if (html.includes(MARKER)) return false; // déjà enrichi
  // Garde : fichiers non-HTML (réponses gzip 404 de HTTrack, endpoint AJAX JSON…)
  //  → ne jamais les réécrire (corruption garantie). On les saute tels quels.
  if (!/<!doctype html|<html/i.test(html) || !/<\/head>/i.test(html)) return false;
  const nl = html.includes('\r\n') ? '\r\n' : '\n';
  const { isHome, isProduct, title, product } = pageData(html, relPath);
  const canonical = canonicalUrl(relPath);

  // Fusion JSON-LD PrestaShop → on retire les blocs "Product" du thème (domaine
  // abîmé steroidskaufen.com, offre en .html) et on récupère leur description/sku
  // pour les réinjecter dans notre bloc Product canonique (un seul @type Product/page).
  let extraDesc = '', extraSku = '', extraPrice = '';
  if (isProduct) {
    const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)];
    for (const b of blocks) {
      if (!/"@type"\s*:\s*"Product"/.test(b[1])) continue;
      try {
        const j = JSON.parse(b[1]);
        let desc = j.description || '';
        // desc = texte ≤ 500 car. sans retours pour alimenter notre bloc
        if (typeof desc === 'string') desc = desc.replace(/\s+/g, ' ').trim().slice(0, 500);
        if (desc) extraDesc = desc;
        if (j.sku) extraSku = j.sku;
        if (!extraPrice && j.offers && j.offers.price) extraPrice = String(j.offers.price).replace(/[^\d.,]/g, '').replace(/\./g, '').replace(',', '.');
      } catch { /* bloc non-JSON (rare) : ignoré */ }
      html = html.split(b[0]).join(''); // retire le bloc PrestaShop
    }
  }

  const headBits = [
    `<script>document.documentElement.classList.add('js');</script>`,
    `<style>html.js .seo-block{display:none}.seo-city-info{background:#f4f4f7;border-radius:8px;padding:16px;margin:24px auto;max-width:1110px}.seo-city-info h2{font-size:1.25rem;color:#1a1a2e;margin:0 0 8px}.seo-city-info p{color:#444;font-size:.95rem;margin:0}</style>`,
    `<meta name="geo.region" content="DE">`,
    `<meta name="geo.placename" content="Deutschland">`,
    `<link rel="canonical" href="${canonical}">`,
    `<link rel="alternate" hreflang="de-DE" href="${canonical}">`,
  ];
  if (!isHome && title && !title.includes('ganz Deutschland')) {
    headBits.push(`<title>${title} – Versand in ganz Deutschland</title>`); // titre enrichi
  }
  if (isHome) {
    const desc = (html.match(/<meta name="description" content="([^"]*)"/i) || [])[1] || '';
    if (desc && !desc.includes('Berlin')) {
      const citiesList = cities.slice(0, 6).map(c => c.name).join(', ');
      headBits.push(`<meta name="description" content="${desc} Schneller und diskreter Versand in ganz Deutschland – auch nach ${citiesList} und viele weitere Städte.">`);
    }
  }

  headBits.push(`<script type="application/ld+json">${JSON.stringify(storeLd(canonical, isProduct && product ? product.image : SHOP_LOGO))}</script>`);

  if (isProduct && product) {
    const prodLd = {
      "@context": "https://schema.org",
      "@type": "Product",
      "name": product.name,
      "url": canonical,
      "image": product.image,
      "offers": {
        "@type": "Offer",
        "url": canonical,
        "priceCurrency": "EUR",
        "price": String(product.price || extraPrice || ''),
        "itemCondition": "https://schema.org/NewCondition",
        "availability": "https://schema.org/InStock"
      }
    };
    if (extraDesc) prodLd.description = extraDesc;
    if (extraSku) prodLd.sku = extraSku;
    headBits.push(`<script type="application/ld+json">${JSON.stringify(prodLd)}</script>`);
  }
  if (isHome) {
    headBits.push(`<script type="application/ld+json">${JSON.stringify({
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": faqs.map(f => ({ "@type": "Question", "name": f.question, "acceptedAnswer": { "@type": "Answer", "text": f.answer } }))
    })}</script>`);
  }

  const headInj = nl + '  <!-- ' + MARKER + ' -->' + nl + '  ' + headBits.filter(Boolean).join(nl + '  ') + nl;

  const bodyBits = [seoCityInfo(), seoCityBlock()];
  if (!isProduct) bodyBits.push(seoPopularBlock());
  if (isHome) bodyBits.push(seoFaqBlock());

  let out = html.replace(/<head>/i, '<head>' + headInj);
  out = out.replace(/<\/body>/i, nl + '<!-- generated by seo-enrich.mjs -->' + nl + bodyBits.join(nl) + nl + '</body>');
  // Migration domaine : toutes les références résiduelles à l'ancien domaine
  // (BreadcrumbList PrestaShop, objet JS prestashop, og:, images…) → domaine actuel.
  out = out.replace(/steroidskaufen\.com/gi, 'steroidskaufen.dealsnows.com');
  writeFileSync(fp, out, 'utf8');
  return true;
}

// ---------- walk ----------
const files = [];
function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const fp = join(dir, e.name);
    if (e.isDirectory()) walk(fp);
    else if (e.name.endsWith('.html')) files.push(fp);
  }
}
walk(DE_DIR);
files.sort();

let enriched = 0;
for (const fp of files.slice(0, limit)) {
  const relPath = relative(DE_DIR, fp).replace(/\\/g, '/');
  if (enrichFile(fp, relPath)) enriched++;
}
console.log(`Résumé : ${enriched} fichiers enrichis sur ${Math.min(files.length, limit)} analysés (total ${files.length}).`);