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
/assets/perspectives.json → source de vérité articles
/articles-publies.md      → journal éditorial de tous les articles
```

## Règles absolues

- **Toujours modifier FR et EN en parallèle** — le FR est la source, l'EN est traduit
- **Jamais de `git push` sans confirmation** de Robin
- **Commits en anglais**, co-signés : `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- **Interdit** : le caractère `—` (tiret cadratin) dans tout contenu créé
- **Python** : `python` (pas `python3`) — Windows

## Règle critique — articles-publies.md

**A chaque publication ou modification d'article, mettre à jour `articles-publies.md` :**

- **Nouvel article** : ajouter l'entrée en tête de liste avec titre FR/EN, slugs, date, catégorie, illustration, angle éditorial
- **Modification d'un article** : mettre à jour le champ `dateModified` et noter les changements apportés

Ce fichier est le journal éditorial du site. Il doit toujours refléter l'état réel des articles publiés.

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

## Workflow — nouvel article

1. Créer `fr/perspectives/[slug-fr].html` et `en/perspectives/[slug-en].html`
2. Créer illustration SVG + OG PNG
3. Meta description unique 150-160 car., og:image, Schema.org complet, bloc "A lire aussi"
4. Ajouter l'entrée dans `assets/perspectives.json`
5. Lancer `python update_home_persp.py`
6. Mettre à jour les deux `perspectives/index.html`
7. Mettre à jour les blocs "A lire aussi" des articles existants
8. Ajouter les URLs dans `sitemap.xml` avec `lastmod` du jour
9. Mettre à jour `llms.txt` et `llms-fr.txt`
10. **Mettre à jour `articles-publies.md`** (nouvelle entrée en tête)
11. Commit + push (après confirmation)
12. IndexNow ping

## Workflow — modification d'un article existant

1. Modifier le fichier FR
2. Traduire et mettre à jour le fichier EN
3. Lancer `python update_home_persp.py` si les cartes home sont impactées
4. **Mettre à jour `articles-publies.md`** (dateModified + note des changements)
5. Commit + push (après confirmation)

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

## Palette CSS

```css
--gold: #9a7228
--cream: #f7f4ee
--cream-dark: #f0ece2
--ink: #1a1712
/* Font : Jost (Google Fonts) */
```

## Problème connu — git fetch

Si `git fetch` echoue avec `refs/desktop.ini` : supprimer les `desktop.ini` dans `.git/` :
```powershell
Get-ChildItem ".git" -Force -Recurse -Filter "desktop.ini" | Remove-Item -Force
```
