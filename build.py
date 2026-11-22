"""Génère le site statique (français à la racine, anglais dans en/) à partir de content/*.json.

    python build.py

Modifier les textes : content/fr.json et content/en.json (même structure).
Réglages (courriel, domaine, formulaire, prise de rendez-vous) : content/site.json.
Les fichiers produits (index.html, en/index.html, 404.html, sitemap.xml, robots.txt, CNAME) sont versionnés :
GitHub Pages les sert tels quels. Aucune dépendance hors de Python 3.9+.
"""
import json
from html import escape
from pathlib import Path
from urllib.parse import quote

RACINE = Path(__file__).resolve().parent
CONTENU = RACINE / 'content'


def e(s):
    return escape(str(s), quote=True)


def charger(nom):
    return json.loads((CONTENU / nom).read_text(encoding='utf-8'))


def url_base(site):
    if site.get('domaine_personnalise'):
        return 'https://' + site['domaine_personnalise'].strip().strip('/').removeprefix('https://') + '/'
    return site['url_du_site'].rstrip('/') + '/'


# ---------- Morceaux de page ----------
def entete(c, p):
    nav = ''.join(f'<li><a href="#{e(n["id"])}">{e(n["libelle"])}</a></li>' for n in c['nav'])
    autre = c['autre']
    lang = (f'<a class="langue" href="{p}{e(autre["dossier"]) or "./"}" hreflang="{e(autre["code"])}" '
            f'lang="{e(autre["code"])}" title="{e(autre["libelle"])}">{e(autre["court"])}</a>')
    return f'''<header class="entete">
  <div class="cadre entete-cadre">
    <a class="marque" href="./"><img src="{p}assets/img/logo.png" width="720" height="123" alt="Duquette Automation"></a>
    <nav class="nav" aria-label="Navigation principale">
      <ul>{nav}</ul>
    </nav>
    {lang}
    <details class="menu-mobile">
      <summary>{e(c["menu"])}</summary>
      <ul>{nav}</ul>
    </details>
  </div>
</header>'''


def apercu_app(c, p):
    """Reproduction fidèle (HTML/CSS) de l'application livrée à Matulu. Données d'exemple."""
    a = c['apercu']
    return f'''<figure class="apercu">
  <div class="fenetre" aria-hidden="true">
    <div class="fenetre-barre"><span>Matulu — Outils de la librairie</span><span class="fenetre-boutons"><i></i><i></i><i></i></span></div>
    <div class="fenetre-corps">
      <div class="app-cote">
        <div class="app-marque">Matulu<small>Librairie</small></div>
        <div class="app-outil">Répartir une réception<small>Après chaque réception</small></div>
        <div class="app-outil actif">Vérifier les commandes clients<small>Chaque matin</small></div>
        <div class="app-outil">Promotions → livres à commander<small>Quand des promos arrivent</small></div>
        <div class="app-signature">
          <p>{e(a["slogan_client"])}</p>
          <span class="app-concu">Conçu par</span>
          <span class="app-concepteur"><img src="{p}assets/img/monogramme.png" alt="" width="120" height="58">Duquette Automation</span>
        </div>
      </div>
      <div class="app-page">
        <div class="app-titre">Vérifier les commandes clients</div>
        <div class="app-texte">Croise les commandes ouvertes avec l’inventaire.</div>
        <div class="app-fichier"><b></b><span>Liste détaillée des commandes<small>Liste commande_2026-11-18.pdf</small></span></div>
        <div class="app-fichier"><b></b><span>Export d’inventaire (CSV)<small>Inv-2026-11-18.csv</small></span></div>
        <div class="app-lancer">Lancer</div>
        <div class="app-resultat">
          <div class="app-resultat-titre">Terminé</div>
          <div>★ 4 commandes prêtes à partir</div>
          <div>⚠ 2 livres à retirer des tablettes</div>
          <div>⚠ 1 exemplaire manquant en inventaire</div>
          <div class="app-excel">Ouvrir le résultat dans Excel</div>
        </div>
      </div>
    </div>
  </div>
  <figcaption>{e(a["legende"])}</figcaption>
</figure>'''


def hero(c, p):
    h = c['hero']
    titre = ''.join(f'<span>{e(l)}</span>' for l in h['titre'])
    return f'''<section class="hero">
  <div class="cadre hero-grille">
    <div class="hero-texte">
      <h1>{titre}</h1>
      <p class="hero-intro">{e(h["texte"])}</p>
      <div class="actions">
        <a class="bouton" href="#contact">{e(h["bouton"])}</a>
        <a class="lien-texte" href="#realisations">{e(h["secondaire"])}</a>
      </div>
      <p class="region">{e(h["region"])}</p>
    </div>
    {apercu_app(c, p)}
  </div>
</section>'''


def services(c):
    s = c['services']
    items = ''.join(f'<li><h3>{e(i["titre"])}</h3><p>{e(i["texte"])}</p></li>' for i in s['items'])
    return f'''<section class="section" id="services" aria-labelledby="t-services">
  <div class="cadre">
    <h2 id="t-services">{e(s["titre"])}</h2>
    <ul class="services">{items}</ul>
    <p class="prix"><strong>{e(s["prix"]["montant"])}</strong> {e(s["prix"]["texte"])}</p>
  </div>
</section>'''


def realisations(c):
    r = c['realisations']
    lib = r['libelles']
    cas = []
    for k in r['cas']:
        outils = ''.join(f'<li><strong>{e(o["nom"])}</strong> : {e(o["texte"])}</li>' if c['lang'] == 'fr'
                         else f'<li><strong>{e(o["nom"])}</strong>: {e(o["texte"])}</li>' for o in k['outils'])
        slogan = ''.join(f'<span>{e(l)}</span>' for l in k['slogan'])
        cas.append(f'''<article class="cas" id="cas-{e(k["id"])}">
      <div class="cas-tete">
        <h3>{slogan}</h3>
        <p class="cas-client"><strong>{e(k["client"])}</strong><br>{e(k["secteur"])}</p>
      </div>
      <dl class="cas-detail">
        <dt>{e(lib["besoin"])}</dt><dd>{e(k["besoin"])}</dd>
        <dt>{e(lib["solution"])}</dt><dd><ul>{outils}</ul></dd>
        <dt>{e(lib["resultat"])}</dt><dd>{e(k["resultat"])}</dd>
      </dl>
    </article>''')
    return f'''<section class="section" id="realisations" aria-labelledby="t-realisations">
  <div class="cadre">
    <h2 id="t-realisations">{e(r["titre"])}</h2>
    <p class="intro">{e(r["intro"])}</p>
    {"".join(cas)}
  </div>
</section>'''


def demarche(c):
    d = c['demarche']
    etapes = ''.join(f'<li><h3>{e(x["titre"])}</h3><p>{e(x["texte"])}</p></li>' for x in d['etapes'])
    return f'''<section class="section" id="demarche" aria-labelledby="t-demarche">
  <div class="cadre">
    <h2 id="t-demarche">{e(d["titre"])}</h2>
    <ol class="etapes">{etapes}</ol>
  </div>
</section>'''


def apropos(c):
    a = c['apropos']
    paras = ''.join(f'<p>{e(x)}</p>' for x in a['paragraphes'])
    return f'''<section class="section apropos" id="a-propos" aria-labelledby="t-apropos">
  <div class="cadre apropos-grille">
    <h2 id="t-apropos">{e(a["titre"])}</h2>
    <div class="apropos-texte">{paras}<p class="signature">{e(a["signature"])}</p></div>
  </div>
</section>'''


def temoignages(c):
    """Section affichée seulement quand content/*.json contient des témoignages.
    Format d'un élément : {"citation": "…", "nom": "…", "role": "…", "entreprise": "…"}"""
    t = c['temoignages']
    if not t['items']:
        return ''
    items = []
    for x in t['items']:
        qui = ', '.join(v for v in (x.get('role', ''), x.get('entreprise', '')) if v)
        items.append(f'<figure class="temoignage"><blockquote><p>{e(x["citation"])}</p></blockquote>'
                     f'<figcaption><strong>{e(x["nom"])}</strong>{"<br>" + e(qui) if qui else ""}</figcaption></figure>')
    return f'''<section class="section" id="temoignages" aria-labelledby="t-temoignages">
  <div class="cadre">
    <h2 id="t-temoignages">{e(t["titre"])}</h2>
    <div class="temoignages">{"".join(items)}</div>
  </div>
</section>'''


def formulaire_action(site):
    """Formspree si un identifiant est fourni ; sinon FormSubmit, qui n'exige aucun compte (le premier message
    envoie un courriel d'activation à l'adresse du site). "formulaire": false dans site.json retire le formulaire."""
    if site.get('formulaire') is False:
        return ''
    if site.get('formspree_id'):
        return f'https://formspree.io/f/{site["formspree_id"]}'
    return f'https://formsubmit.co/ajax/{site["courriel"]}'


def contact(c, site):
    k = c['contact']
    f = k['formulaire']
    courriel = site['courriel']
    mailto = f'mailto:{courriel}?subject={quote(k["sujet"])}'
    rdv = ''
    if site.get('lien_rendez_vous'):
        rdv = (f'<div class="contact-rdv"><p>{e(k["rendez_vous_texte"])}</p>'
               f'<a class="bouton bouton-clair" href="{e(site["lien_rendez_vous"])}" target="_blank" rel="noopener">'
               f'{e(k["rendez_vous"])}</a></div>')
    form = ''
    action = formulaire_action(site)
    if action:
        form = f'''<form class="formulaire" action="{e(action.replace('/ajax/', '/'))}" data-ajax="{e(action)}" method="POST"
          data-envoi="{e(f["envoi"])}" data-succes="{e(f["succes"])}" data-erreur="{e(f["erreur"])} {e(courriel)}.">
      <h3>{e(f["titre"])}</h3>
      <div class="champs-duo">
        <label><span>{e(f["nom"])}</span><input name="nom" autocomplete="name" required></label>
        <label><span>{e(f["entreprise"])} <span class="facultatif">({e(f["facultatif"])})</span></span><input name="entreprise" autocomplete="organization"></label>
      </div>
      <label><span>{e(f["courriel"])}</span><input type="email" name="email" autocomplete="email" required></label>
      <label><span>{e(f["message"])}</span><textarea name="message" rows="5" required></textarea></label>
      <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="piege" aria-hidden="true">
      <input type="text" name="_honey" tabindex="-1" autocomplete="off" class="piege" aria-hidden="true">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_subject" value="{e(k["sujet"])}">
      <button class="bouton" type="submit">{e(f["envoyer"])}</button>
      <p class="formulaire-etat" role="status" aria-live="polite"></p>
    </form>'''
    droite = form + rdv
    return f'''<section class="section contact" id="contact" aria-labelledby="t-contact">
  <div class="cadre contact-grille{" contact-seul" if not droite else ""}">
    <div class="contact-texte">
      <h2 id="t-contact">{e(k["titre"])}</h2>
      <p>{e(k["texte"])}</p>
      <p class="contact-courriel"><span>{e(k["par_courriel"])}</span><a href="{e(mailto)}">{e(courriel)}</a></p>
      <a class="bouton" href="{e(mailto)}">{e(k["bouton_courriel"])}</a>
    </div>
    {f'<div class="contact-options">{droite}</div>' if droite else ''}
  </div>
</section>'''


def pied(c, p, site):
    autre = c['autre']
    return f'''<footer class="pied">
  <div class="cadre pied-grille">
    <img src="{p}assets/img/logo-blanc.png" width="720" height="123" alt="Duquette Automation">
    <p class="pied-slogan">{e(c["pied"]["slogan"])}</p>
    <p class="pied-liens"><a href="mailto:{e(site["courriel"])}">{e(site["courriel"])}</a>
      <a href="{p}{e(autre["dossier"]) or "./"}" hreflang="{e(autre["code"])}" lang="{e(autre["code"])}">{e(autre["libelle"])}</a></p>
    <p class="pied-droits">© {site["annee"]} {e(site["nom"])}. {e(c["pied"]["droits"])}</p>
  </div>
</footer>'''


def tete(c, p, site, base, titre=None, indexer=True):
    m = c['meta']
    fr, en = base, base + 'en/'
    ici = base + c['dossier']
    return f'''<!DOCTYPE html>
<html lang="{c["lang"]}-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre or m["titre"])}</title>
<meta name="description" content="{e(m["description"])}">
{'' if indexer else '<meta name="robots" content="noindex">'}
<link rel="canonical" href="{e(ici)}">
<link rel="alternate" hreflang="fr-CA" href="{e(fr)}">
<link rel="alternate" hreflang="en-CA" href="{e(en)}">
<link rel="alternate" hreflang="x-default" href="{e(fr)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(site["nom"])}">
<meta property="og:title" content="{e(m["titre"])}">
<meta property="og:description" content="{e(m["description"])}">
<meta property="og:url" content="{e(ici)}">
<meta property="og:image" content="{e(base)}assets/img/icon-512.png">
<meta property="og:locale" content="{c["locale"]}">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
<link rel="preload" href="{p}assets/fonts/fira-sans-semibold.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="{p}assets/fonts/fira-sans-regular.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
<script type="application/ld+json">{json.dumps({
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": site["nom"], "url": base,
        "email": site["courriel"], "slogan": c["pied"]["slogan"], "description": m["description"],
        "areaServed": ["Nouveau-Brunswick", "Québec", "Canada"], "logo": base + "assets/img/icon-512.png",
        "founder": {"@type": "Person", "name": "Thomas Duquette"}}, ensure_ascii=False).replace("</", "<\\/")}</script>
</head>'''


def page(c, site, base):
    p = '../' if c['dossier'] else ''
    return f'''{tete(c, p, site, base)}
<body>
<a class="evitement" href="#contenu">{e(c["lien_evitement"])}</a>
{entete(c, p)}
<main id="contenu">
{hero(c, p)}
{services(c)}
{realisations(c)}
{demarche(c)}
{apropos(c)}
{temoignages(c)}
{contact(c, site)}
</main>
{pied(c, p, site)}
{'<script src="' + p + 'assets/js/site.js" defer></script>' if formulaire_action(site) else ''}
</body>
</html>
'''


def page_404(fr, en, site, base):
    """404 bilingue ; liens absolus (la page peut être servie à n'importe quelle profondeur)."""
    p = base
    a, b = fr['page_404'], en['page_404']
    return f'''{tete(fr, p, site, base, titre=a["titre"] + " — " + site["nom"], indexer=False)}
<body class="page-404">
<main class="cadre erreur-404">
  <a href="{e(base)}"><img src="{e(base)}assets/img/logo.png" width="360" height="62" alt="Duquette Automation"></a>
  <h1>{e(a["titre"])}</h1><p>{e(a["texte"])} <a href="{e(base)}">{e(a["lien"])}</a></p>
  <h2 lang="en">{e(b["titre"])}</h2><p lang="en">{e(b["texte"])} <a href="{e(base)}en/">{e(b["lien"])}</a></p>
</main>
</body>
</html>
'''


def main():
    site = charger('site.json')
    fr, en = charger('fr.json'), charger('en.json')
    base = url_base(site)
    (RACINE / 'index.html').write_text(page(fr, site, base), encoding='utf-8', newline='\n')
    (RACINE / 'en').mkdir(exist_ok=True)
    (RACINE / 'en' / 'index.html').write_text(page(en, site, base), encoding='utf-8', newline='\n')
    (RACINE / '404.html').write_text(page_404(fr, en, site, base), encoding='utf-8', newline='\n')
    (RACINE / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n', encoding='utf-8')
    (RACINE / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + ''.join(f'  <url><loc>{u}</loc>'
                  f'<xhtml:link rel="alternate" hreflang="fr-CA" href="{base}"/>'
                  f'<xhtml:link rel="alternate" hreflang="en-CA" href="{base}en/"/></url>\n' for u in (base, base + 'en/'))
        + '</urlset>\n', encoding='utf-8')
    cname = RACINE / 'CNAME'
    if site.get('domaine_personnalise'):
        cname.write_text(site['domaine_personnalise'].strip() + '\n', encoding='utf-8')
    elif cname.exists():
        cname.unlink()
    print(f'Site généré pour {base}')


if __name__ == '__main__':
    main()
