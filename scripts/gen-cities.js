// Génère les pages villes "served area" pour steroidskaufen.dealsnows.com
// Base = de/kontakt.html (squelette header/footer/CSS/JS propres à PrestaShop)
const fs = require('fs');
const path = require('path');
const ROOT = 'C:/clone-allemagne-v2/steroidskaufen-seo';
const BASE = path.join(ROOT, 'de/kontakt.html');

// ─── Données villes ───
const CITIES = [
  { slug:'steroide-kaufen-berlin',      name:'Berlin',            land:'Berlin',                 landCode:'BE', region:'Berlin-Brandenburg',              pop:'3,7 Millionen', areaServed:'Berlin'},
  { slug:'steroide-kaufen-hamburg',     name:'Hamburg',           land:'Hamburg',                landCode:'HH', region:'Hamburg',                       pop:'1,9 Millionen', areaServed:'Hamburg'},
  { slug:'steroide-kaufen-muenchen',    name:'München',           land:'Bayern',                 landCode:'BY', region:'Bayern',                        pop:'1,5 Millionen', areaServed:'München'},
  { slug:'steroide-kaufen-koeln',       name:'Köln',              land:'Nordrhein-Westfalen',    landCode:'NW', region:'Nordrhein-Westfalen',          pop:'1,1 Millionen', areaServed:'Köln'},
  { slug:'steroide-kaufen-frankfurt-am-main', name:'Frankfurt am Main', land:'Hessen',          landCode:'HE', region:'Hessen',                       pop:'770.000',       areaServed:'Frankfurt am Main'},
  { slug:'steroide-kaufen-stuttgart',   name:'Stuttgart',         land:'Baden-Württemberg',      landCode:'BW', region:'Baden-Württemberg',            pop:'630.000',       areaServed:'Stuttgart'},
  { slug:'steroide-kaufen-duesseldorf', name:'Düsseldorf',        land:'Nordrhein-Westfalen',    landCode:'NW', region:'Nordrhein-Westfalen',          pop:'620.000',       areaServed:'Düsseldorf'},
  { slug:'steroide-kaufen-leipzig',     name:'Leipzig',           land:'Sachsen',                landCode:'SN', region:'Sachsen',                      pop:'620.000',       areaServed:'Leipzig'},
  { slug:'steroide-kaufen-hannover',    name:'Hannover',          land:'Niedersachsen',          landCode:'NI', region:'Niedersachsen',                pop:'570.000',       areaServed:'Hannover'},
  { slug:'steroide-kaufen-dortmund',    name:'Dortmund',          land:'Nordrhein-Westfalen',    landCode:'NW', region:'Nordrhein-Westfalen',          pop:'590.000',       areaServed:'Dortmund'},
];
const DOMAIN = 'https://steroidskaufen.dealsnows.com';

// ─── Produits d'ancrage réels (nom + URL prod) ───
const PRODUCTS = [
  {name:'10 x Olimp Somatropin 100 IU',        url:'/de/wachstumshormone/544-10-x-olimp-somatropin-100-iu'},
  {name:'2 x DepreStop EVO Meds + 1 GRATIS',   url:'/de/evo-meds/466-2-x-deprestop-evo-meds-1-free'},
  {name:'2 x Endogenic Kisspeptin + 1 GRATIS', url:'/de/kisspeptin/465--2-x-endogenic-kisspeptin-1-free'},
  {name:'2 x Olimp Somatropin 100 IU + 1 GRATIS', url:'/de/wachstumshormone/461-2-x-olimp-somatropin-100-iu-1-free'},
  {name:'2 x Parabolan + 1 GRATIS',            url:'/de/injizierbare-steroide/456-2-x-parabolan-1-free'},
  {name:'2 x Tiromel T3 + 1 GRATIS',           url:'/de/fatburner/462-2-x-tiromel-t3-1-free'},
  {name:'3 x Retatrutide 4Mg Pen',             url:'/de/fatburner/550-3-x-retatrutide-4mg-pen'},
  {name:'3 x Retatrutide 8Mg Pen',             url:'/de/fatburner/546-3-x-retatrutide-8mg-pen'},
  {name:'3 x Sema G 2 MG',                     url:'/de/fatburner/548-3-x-sema-g-2-mg'},
  {name:'3 x Sema+Cagri Pen 2 + 2 MG',         url:'/de/fatburner/549--3-x-semacagri-pen-2-2-mg'},
  {name:'3 x Semaglutid 3 mg 30 tabs',         url:'/de/fatburner/551-3-x-semaglutid-3-mg-30-tabs'},
  {name:'3 x Semaglutid 4 Mg',                 url:'/de/fatburner/545-3-x-semaglutid-4-mg'},
];

function rotateProducts(seed){
  // sélection de 8 produits, rotation selon l'index de la ville pour différencier
  const n = PRODUCTS.length, take = 8;
  const out = [];
  for(let i=0;i<take;i++) out.push(PRODUCTS[(seed+i)%n]);
  return out;
}

const CITY_STYLE = `<style>
.stk-city{max-width:1110px;margin:0 auto;padding:8px 2px}
.stk-city h1{font-size:1.8rem;color:#1a1a2e;margin:0 0 12px;line-height:1.25}
.stk-city__lead{color:#333;font-size:1.05rem;line-height:1.6;margin:0 0 20px}
.stk-city__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:0 0 24px}
.stk-city__card{background:#fff;border:1px solid #e6e6ea;border-radius:8px;padding:14px 16px}
.stk-city__card b{display:block;color:#1a1a2e;margin-bottom:4px}
.stk-city__card span{color:#555;font-size:.92rem;line-height:1.5;display:block}
.stk-city__cta{display:inline-block;background:#1a1a2e;color:#fff!important;text-decoration:none;font-weight:600;padding:12px 22px;border-radius:6px;margin:4px 0 8px}
.stk-city__cta:hover{background:#333}
.stk-city__note{color:#666;font-size:.85rem;margin:0 0 24px}
.stk-city__cities{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none}
.stk-city__cities a{display:inline-block;background:#f4f4f7;border-radius:6px;padding:8px 14px;color:#1a1a2e;text-decoration:none}
.stk-city__cities a:hover{background:#e8e8ee}
</style>`;

function buildCity(c, seed){
  const base = fs.readFileSync(BASE,'utf8');
  const url = DOMAIN + '/de/' + c.slug;
  const prods = rotateProducts(seed);
  const prodsListHtml = prods.map(p=>`        <li><a href="${p.url}">${p.name}</a></li>`).join('\n');
  const townNames = CITIES.map(x=>x).filter(x=>x.slug!==c.slug);
  const landInNote = c.land !== c.name ? ` (${c.land})` : '';

  // ── Métadescriptions (allemand, ~150 char) ──
  const title1 = `Steroide kaufen in ${c.name} | Steroidekaufen.com – diskrete Lieferung`;
  const title2 = `Steroide kaufen in ${c.name} | Steroidekaufen.com`;
  const desc = `Steroide online kaufen in ${c.name}. Diskrete und schnelle Lieferung in ${c.name} (${c.land}) und Umgebung. Auswahl, sichere Verpackung, deutscher Support.`;

  // ── Contenu central (remplace wrapper→footer) ──
  const cityContent = `<section id="wrapper">
    <div class="container">
      <nav data-depth="2" class="breadcrumb">
  <ol>
    <li><a href="index.html"><span>Steroide kaufen</span></a></li>
    <li><a href="${c.slug}.html"><span>Steroide kaufen in ${c.name}</span></a></li>
  </ol>
</nav>
      <div class="row">
        <div id="content-wrapper" class="col-xs-12 col-sm-12">
          <section id="main">
            <section id="content" class="page-content card card-block">
              ${CITY_STYLE}
              <div class="stk-city">
                <h1 id="city-name">Steroide kaufen in ${c.name}</h1>
                <p class="stk-city__lead">Sie suchen in ${c.name}${landInNote} nach anabolen Steroiden und SARM-Präparaten? Unser Online-Shop liefert diskret und schnell in ${c.name}${landInNote} sowie in die umliegenden Städte. Egal ob Sie in ${c.name} im Zentrum oder in den Randbezirken wohnen – Ihre Bestellung erreicht Sie zuverlässig und neutral verpackt.</p>

                <div class="stk-city__grid">
                  <div class="stk-city__card"><b>Bevölkerung</b><span>${c.name} zählt etwa ${c.pop} Einwohner und ist das Zentrum der Region ${c.region}.</span></div>
                  <div class="stk-city__card"><b>Diskrete Lieferung</b><span>Neutrale Verpackung ohne Absender-Vermerk – Ihre Privatsphäre bleibt in ${c.name} vollständig geschützt.</span></div>
                  <div class="stk-city__card"><b>Versand in ${c.name}</b><span>Express- und Standardversand nach ${c.name}. Lieferzeit in der Regel 2–4 Werktage innerhalb von ${c.land}.</span></div>
                  <div class="stk-city__card"><b>Deutscher Support</b><span>Persönliche Beratung vor Ihrer Bestellung – direkt erreichbar aus ${c.name} und Umgebung.</span></div>
                </div>

                <a class="stk-city__cta" href="/de/2-steroide">Zum kompletten Sortiment</a>
                <p class="stk-city__note">Hinweis: Wir führen kein Ladengeschäft in ${c.name} – unser Service ist ein diskreter Online-Versandhandel für ganz ${c.land}.</p>

                <h2>Beliebte Produkte in ${c.name}</h2>
                <ul class="seo-block__list">
${prodsListHtml}
                </ul>

                <h2>Weitere Liefergebiete</h2>
                <ul class="stk-city__cities">
                  ${townNames.map(t=>`<li><a href="/de/${t.slug}">Steroide kaufen in ${t.name}</a></li>`).join('\n                  ')}
                </ul>
              </div>
            </section>
          </section>
        </div>
      </div>
    </div>
  </section>`;

  const innerStart = base.indexOf('<section id="wrapper">');
  const innerEnd   = base.indexOf('<footer id="footer">');
  let page = base.slice(0, innerStart) + cityContent + base.slice(innerEnd);

  // ── Remplacements <head> ──
  // geo
  page = page.replace('<meta name="geo.region" content="DE">', `<meta name="geo.region" content="DE-${c.landCode}">`);
  page = page.replace('<meta name="geo.placename" content="Deutschland">', `<meta name="geo.placename" content="${c.name}">`);
  // canonical / hreflang absolus
  page = page.split('/de/kontakt').join('/de/' + c.slug);
  // OnlineStore url (slash échappés)
  page = page.split('steroidskaufen.dealsnows.com\\/de\\/kontakt').join('steroidskaufen.dealsnows.com\\/de\\/' + c.slug);
  // titres — remplace TOUS les <title> (le 1er sert de document title côté Google)
  page = page.replace(/<title>[\s\S]*?<\/title>/g, `<title>${title2}</title>`);
  // méta description
  page = page.replace('content="Nutzen Sie unser Kontaktformular"', `content="${desc}"`);
  // canonical / hreflang relatifs + lien dropdown langue
  page = page.split('href="kontakt.html"').join(`href="${c.slug}.html"`);
  // Hygiene nouvelle page : le bloc relatif du theme PrestaShop (canonical + hreflang)
  // pointe vers <slug>.html → on le rend absolu (extensible). Le breadcrumb garde son href .html.
  page = page.replace(`rel="canonical" href="${c.slug}.html"`, `rel="canonical" href="${url}"`)
             .replace(`href="${c.slug}.html" hreflang="de"`, `href="${url}" hreflang="de"`)
             .replace(`href="${c.slug}.html" hreflang="x-default"`, `href="${url}" hreflang="x-default"`);
  // alternates es/nl : pas de page ville équivalente → retirer (cluster hreflang invalide)
  page = page.replace(`<link rel="alternate" href="https://steroidskaufen.dealsnows.com/es/contacto" hreflang="es"/>`, '')
              .replace(`<link rel="alternate" href="https://steroidskaufen.dealsnows.com/nl/contact-opnemen" hreflang="nl"/>`, '');
  // Un seul <title> dans le head : garder le premier (enrichi), retirer les suivants.
  const allTitles = page.match(/<title>[\s\S]*?<\/title>/g) || [];
  for (let i = 1; i < allTitles.length; i++) {
    const t = allTitles[i], first = allTitles[0];
    const start = page.indexOf(t, page.indexOf(first) + first.length);
    if (start !== -1) page = page.slice(0, start) + page.slice(start + t.length);
  }
  // body class/id
  page = page.replace('<body id="contact"', `<body id="city-page"`);
  // OnlineStore areaServed → conjugue la ville
  page = page.replace('"areaServed":{"@type":"Country","name":"Deutschland"}', `"areaServed":[{"@type":"City","name":"${c.name}"},{"@type":"Country","name":"Deutschland"}]`);

  // ── BreadcrumbList JSON-LD : supprime l'ancien bloc (entier, y compris {"@context") puis ré-injecte proprement ──
  page = page.replace(/<script type="application\/ld\+json">\{"@context":"https:\/\/schema.org","@type":"BreadcrumbList"[\s\S]*?<\/script>/, '');
  const bcJson = {
    "@context":"https://schema.org","@type":"BreadcrumbList",
    "itemListElement":[
      {"@type":"ListItem","position":1,"name":"Steroide kaufen","item":DOMAIN+"/de/"},
      {"@type":"ListItem","position":2,"name":("Steroide kaufen in "+c.name),"item":url}
    ]
  };

  // ── ItemList JSON-LD (produits populaires) + OnlineStore url final ──
  const itemList = {
    "@context":"https://schema.org","@type":"ItemList",
    "name": `Beliebte Produkte in ${c.name}`,
    "itemListElement": prods.map((p,i)=>({"@type":"ListItem","position":i+1,"name":p.name,"url":DOMAIN+p.url}))
  };
  // injecte ItemList + BreadcrumbList juste avant </head>
  const extraJson = [bcJson, itemList].map(j=>'  <script type="application/ld+json">'+JSON.stringify(j)+'</script>').join('\n');
  page = page.replace('</head>', extraJson+'\n    </head>');

  // ── Blocs seo de fin (city-info + popular + cart.js) ──
  const tailMark = '<!-- generated by seo-enrich.mjs -->';
  const tailIdx = page.indexOf(tailMark);
  if (tailIdx !== -1){
    const bodyEnd = page.indexOf('</body>', tailIdx);
    const tailCity = `${tailMark}
<section class="seo-city-info">
    <h2 class="seo-city-info__title">Wir liefern diskret in ${c.name} und in ganz ${c.land}</h2>
    <p class="seo-city-info__text">Bestellen Sie bequem online in unserem Steroide-Shop &ndash; diskreter und schneller Versand in ${c.name} und alle ${c.land}-Regionen wie ${CITIES.map(x=>x.name).join(', ')}.</p>
  </section>`;
    // products list in tail (specific city selection)
    const cityProducts = prods.map(p=>`        <li><a href="${p.url}">${p.name}</a></li>`).join('\n');
    const tailProds = `<section class="seo-block seo-popular">
    <h2 class="seo-block__title">Beliebte Produkte</h2>
    <ul class="seo-block__list">
${cityProducts}
    </ul>
  </section>`;
    page = page.slice(0, tailIdx) + tailCity + '\n' + tailProds + '\n' + page.slice(bodyEnd);
  }

  // ── Écriture ──
  const out = path.join(ROOT, 'de', c.slug + '.html');
  fs.writeFileSync(out, page, 'utf8');
  console.log('OK', c.slug, '->', out, (page.length/1024).toFixed(0)+'KB');
}

CITIES.forEach((c,i)=>buildCity(c,i));
console.log('TERMINÉ', CITIES.length, 'pages.');