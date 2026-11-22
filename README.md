# Site web de Duquette Automation

Site statique bilingue (français à la racine, anglais dans `en/`), servi gratuitement par GitHub Pages.
Aucun cadriciel : un script Python génère les pages à partir des textes.

## Modifier le site

1. Textes : `content/fr.json` et `content/en.json` (même structure). Réglages : `content/site.json`.
2. `python build.py` régénère `index.html`, `en/index.html`, `404.html`, `sitemap.xml`, `robots.txt` (et `CNAME`).
3. Aperçu local : `python -m http.server` puis http://localhost:8000.
4. Commit + push sur `main` : GitHub Pages publie en une minute.

Style : `assets/css/site.css`. Police : Fira Sans (licence SIL OFL, `assets/fonts/OFL.txt`), hébergée sur le site.

### Ajouter une réalisation

Ajouter un bloc dans `realisations.cas` des deux fichiers JSON. `slogan` = la phrase adaptée au client
(« Vous êtes … » + « On s’occupe du reste. »), la même que dans son application. Obtenir l’accord du client avant
de publier son nom.

### Ajouter un témoignage

Dans `temoignages.items` des deux fichiers :

```json
{"citation": "…", "nom": "Prénom Nom", "role": "Propriétaire", "entreprise": "Librairie Matulu"}
```

La section « Ce qu’en disent les clients » n’apparaît que lorsqu’il y a au moins un témoignage.

## Réglages (`content/site.json`)

| Clé | Rôle |
|---|---|
| `courriel` | Adresse affichée et destinataire du formulaire |
| `url_du_site` | Adresse GitHub Pages (balises canoniques, plan du site) |
| `domaine_personnalise` | Ex. `duquetteautomation.ca` : crée le fichier `CNAME` et remplace `url_du_site` partout |
| `formulaire` | `false` retire le formulaire de contact |
| `formspree_id` | Vide = FormSubmit (aucun compte). Avec un identifiant Formspree, le formulaire passe par Formspree |
| `lien_rendez_vous` | Lien Calendly ou Cal.com : ajoute « Réserver un appel » (rien ne s’affiche s’il est vide) |

**Formulaire** : avec FormSubmit, le tout premier message envoyé déclenche un courriel d’activation à
`courriel`. Cliquer le lien une fois ; les messages suivants arrivent directement.

## Mise en ligne (une seule fois)

Dépôt GitHub → *Settings* → *Pages* → *Source* : **Deploy from a branch**, branche `main`, dossier `/ (root)`.
Le site sera à `https://duquette-automation.github.io/Duquette-Automation-Website/`.

### Domaine à soi (plus tard)

1. Acheter le domaine, puis mettre `domaine_personnalise` dans `site.json`, `python build.py`, push.
2. Chez le registraire : quatre enregistrements `A` sur `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153`, et un `CNAME` `www` → `duquette-automation.github.io`.
3. GitHub → *Settings* → *Pages* : le domaine apparaît ; cocher **Enforce HTTPS** quand c’est possible.
