# duale-cv — Instructions Claude Code

Site CV de Robin Dualé. Statique HTML/CSS/JS pur, bilingue FR/EN, déployé sur GitHub Pages.
Production : https://cv-robin.duale.fr

## Stack & structure

```
/fr/                      → pages françaises
/en/                      → pages anglaises
/fr/perspectives/         → index + articles FR
/en/perspectives/         → index + articles EN
/assets/css/main.css      → feuille de style unique
/assets/js/main.js        → JS unique
/assets/js/persp-nav.js   → navigation dynamique (À lire aussi, prev/next) — lit perspectives.json
/assets/perspectives.json → source de vérité articles (titre, sous-titre, slug, date, image, excerpt)
/articles-publies.md      → journal éditorial de tous les articles
/admin/index.html         → panel admin (édition FR + commit GitHub via token)
/update_home_persp.py     → script Python : regénère les 3 cartes home FR + EN depuis perspectives.json
/sitemap.xml              → sitemap SEO
/llms.txt                 → contexte GEO anglais (pour LLMs)
/llms-fr.txt              → contexte GEO français (pour LLMs)
```

## Règles absolues

- **Toujours modifier FR et EN en parallèle** — le FR est la source, l'EN est traduit fidèlement
- **Jamais de `git push` sans confirmation** de Robin
- **Commits en anglais**, co-signés : `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- **Interdit** : le caractère `—` (tiret cadratin) dans tout contenu créé
- **Python** : `python` (pas `python3`) — Windows
- **Ne jamais modifier** les pages parcours/track-record depuis le contenu éditorial

## Synchronisation locale — à faire en début de session

L'admin panel peut avoir commité directement sur GitHub entre deux sessions :

```powershell
git fetch origin
git pull origin main
```

Si divergence (commits locaux non pushés + commits distants) :
```powershell
git stash && git pull --rebase && git stash pop
```

---

## Règle critique — articles-publies.md

**A chaque publication ou modification d'article, mettre à jour `articles-publies.md` :**

- **Nouvel article** : ajouter l'entrée en tête de liste avec titre FR/EN, slugs, date, catégorie, illustration, angle éditorial
- **Modification d'un article** : mettre à jour le champ `dateModified` et noter les changements apportés

Ce fichier est le journal éditorial du site. Il doit toujours refléter l'état réel des articles publiés.

---

## Convention titre à deux niveaux (H1 + cartes)

Chaque article utilise un titre en deux niveaux visuels :

- **Niveau 1 (noir)** : titre principal — `title_fr` / `title_en` dans `perspectives.json`
- **Niveau 2 (or italique)** : sous-titre/accroche — `subtitle_fr` / `subtitle_en` dans `perspectives.json`

### Dans le H1 de l'article HTML

```html
<h1 class="page-title">Titre principal,<br><em>sous-titre accroche.</em></h1>
```

### Dans `perspectives.json`

```json
{
  "title_fr": "Titre principal,",
  "subtitle_fr": "sous-titre accroche.",
  "title_en": "Main title:",
  "subtitle_en": "hook subtitle."
}
```

- `subtitle_fr` / `subtitle_en` peuvent être vides (`""`) si l'article n'a pas de sous-titre
- `persp-nav.js` et `update_home_persp.py` génèrent automatiquement le rendu deux niveaux dans les cartes
- Dans la sidebar (article précédent/suivant), seul le titre principal est affiché

---

## Workflow — nouvel article (checklist complète)

### 1. Fichiers article

- Créer `fr/perspectives/[slug-fr].html` et `en/perspectives/[slug-en].html`
- Copier un article existant comme base, ne pas réinventer la structure
- **Utiliser le texte exact fourni par Robin** — ne jamais réécrire le contenu

### 2. Illustration

- Illustration article : `/assets/illus-[nom].jpg` (800x420) ou SVG
- OG image : `/assets/illus-[nom]-og.png` (1200x630) — générer avec PIL :

```python
from PIL import Image
img = Image.open("assets/illus-[nom].jpg")
img_resized = img.resize((1200, 630))
img_resized.save("assets/illus-[nom]-og.png")
```

### 3. SEO / meta obligatoires (FR + EN)

- `<meta name="description">` — unique, 150-160 car., contenu réel de l'article
- `<meta property="og:description">` — peut être identique ou légèrement différent
- `<meta property="og:image">` et `<meta name="twitter:image">` → `illus-[nom]-og.png`
- `<link rel="canonical">` — URL absolue de la page
- `<link rel="alternate" hreflang="fr">` et `hreflang="en"` — dans les deux versions

### 4. Schema.org (deux blocs JSON-LD obligatoires)

**BreadcrumbList** :
```json
{"@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://cv-robin.duale.fr/fr/"},
  {"@type": "ListItem", "position": 2, "name": "Perspectives", "item": "https://cv-robin.duale.fr/fr/perspectives/"},
  {"@type": "ListItem", "position": 3, "name": "[Titre]", "item": "https://cv-robin.duale.fr/fr/perspectives/[slug].html"}
]}
```

**BlogPosting** — champs obligatoires : `headline`, `wordCount`, `articleSection`, `description`, `datePublished`, `dateModified`, `image`, `mainEntityOfPage`, `author`, `publisher`, `url`, `inLanguage`, `keywords`

### 5. perspectives.json

Ajouter l'entrée en fin de tableau :
```json
{
  "slug_fr": "...", "slug_en": "...",
  "title_fr": "Titre principal,", "subtitle_fr": "sous-titre accroche.",
  "title_en": "Main title:", "subtitle_en": "hook subtitle.",
  "tags_fr": "Tag1 · Tag2", "tags_en": "Tag1 · Tag2",
  "date_fr": "1 jan. 2026", "date_en": "Jan 1, 2026",
  "image_fr": "/assets/illus-[nom].jpg", "image_en": "/assets/illus-[nom]-en.jpg",
  "alt_fr": "...", "alt_en": "...",
  "excerpt_fr": "...", "excerpt_en": "..."
}
```

### 6. Mise à jour des fichiers existants

```
python update_home_persp.py          → regénère les 3 cartes home FR + EN
fr/perspectives/index.html           → la grille est générée par persp-nav.js (rien à faire manuellement)
en/perspectives/index.html           → idem
sitemap.xml                          → ajouter les 2 URLs avec lastmod du jour
llms.txt + llms-fr.txt               → ajouter titre + URL + excerpt de l'article
articles-publies.md                  → nouvelle entrée en tête (antéchronologique)
```

**Note** : les blocs "À lire aussi" et la navigation prev/next sont gérés automatiquement par `persp-nav.js` — aucune modification manuelle dans les articles existants.

### 7. Commit + push (après confirmation Robin)

### 8. IndexNow ping (après push)

```powershell
$body = @{
  host        = "cv-robin.duale.fr"
  key         = "A8A911547D7C17BDDBE856B293F83A46"
  keyLocation = "https://cv-robin.duale.fr/A8A911547D7C17BDDBE856B293F83A46.txt"
  urlList     = @(
    "https://cv-robin.duale.fr/fr/",
    "https://cv-robin.duale.fr/en/",
    "https://cv-robin.duale.fr/fr/perspectives/[slug-fr].html",
    "https://cv-robin.duale.fr/en/perspectives/[slug-en].html"
  )
} | ConvertTo-Json
Invoke-WebRequest -Uri "https://api.indexnow.org/indexnow" -Method POST -ContentType "application/json; charset=utf-8" -Body $body -UseBasicParsing
```

---

## Workflow — modification d'un article existant

### Via l'admin panel (`/admin/index.html`)

L'admin édite uniquement le FR et commite directement sur GitHub.
Après une modif via admin : **toujours faire `git pull` avant de travailler en local**.

### Checklist après toute modification

1. `git pull origin main` — récupérer la version admin si modifiée en ligne
2. Modifier le fichier FR (ou récupérer la version admin)
3. Traduire fidèlement et mettre à jour le fichier EN
4. Vérifier que `dateModified` est mis à jour dans le Schema.org du HTML (FR + EN)
5. Lancer `python update_home_persp.py` si l'article est dans les 3 plus récents
6. Mettre à jour `sitemap.xml` (`lastmod` du jour sur les 2 URLs)
7. Mettre à jour `llms.txt` et `llms-fr.txt` si le contenu a changé significativement
8. **Mettre à jour `articles-publies.md`** (dateModified + note des changements)
9. Commit + push (après confirmation Robin)
10. IndexNow ping sur les URLs modifiées

---

## Admin panel — fonctionnement

`/admin/index.html` — éditeur FR uniquement, accessible via token GitHub.

- **Lit** : le fichier HTML FR depuis GitHub API
- **Édite** : titre principal (noir), sous-titre/accroche (or italique), meta description, corps de l'article
- **Commite** directement sur GitHub (branch `main`)
- **Ne traduit pas** l'EN — à faire manuellement via Claude Code après

Quand Robin dit "j'ai modifié via l'admin" : faire `git pull`, comparer FR vs EN, retraduire si nécessaire.

---

## Noms de fichiers EN — nav critique

Les pages EN ont des noms différents des pages FR. Utiliser **exactement** ces chemins dans le nav des articles EN :

```
/en/                        → Home
/en/about.html              → About
/en/track-record.html       → Career  ⚠️ (pas career.html)
/en/references.html         → Testimonials  ⚠️ (pas testimonials.html)
/en/perspectives/           → Perspectives
/en/contact.html            → Contact
```

---

## Positionnement éditorial

- **Secteurs** : BtoC ou B2B, SaaS, Data, e-commerce
- **Contextes** : PE (private equity), family office
- **Ne pas modifier** : pages parcours/track-record (positionnement figé)
- **Modifier si besoin** : CTAs articles, sidebars articles, llms.txt, llms-fr.txt

---

## Palette CSS

```css
--gold: #9a7228
--cream: #f7f4ee
--cream-dark: #f0ece2
--ink: #1a1712
/* Font : Jost (Google Fonts) */
```

---

## Problème connu — git fetch

Si `git fetch` echoue avec `refs/desktop.ini` : supprimer les `desktop.ini` dans `.git/` :
```powershell
Get-ChildItem ".git" -Force -Recurse -Filter "desktop.ini" | Remove-Item -Force
```
