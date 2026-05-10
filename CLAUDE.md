# duale-cv — Instructions Claude Code

Site CV de Robin Dualé. Statique HTML/CSS/JS pur, bilingue FR/EN, déployé sur GitHub Pages.
Production : https://cv-robin.duale.fr

## Stack & structure

```
/fr/                         → pages françaises
/en/                         → pages anglaises
/fr/perspectives/            → index + articles FR
/en/perspectives/            → index + articles EN
/assets/css/main.css         → feuille de style unique
/assets/js/main.js           → JS unique
/assets/js/persp-nav.js      → navigation dynamique (À lire aussi, prev/next) — lit perspectives.json
/assets/perspectives.json    → source de vérité articles (titre, sous-titre, slug, date, image, excerpt)
/articles-publies.md         → journal éditorial de tous les articles
/admin/index.html            → panel admin (édition FR uniquement + commit GitHub via token)
/update_home_persp.py        → script Python : regénère les 3 cartes home FR + EN depuis perspectives.json
/new_article.py              → script Python : crée l'article FR en draft (noindex, hors sitemap)
/publish_article.py          → script Python : publie le draft (retire noindex, met à jour tous les fichiers)
/article_input.example.json  → modèle de fichier d'input pour new_article.py et publish_article.py
/sitemap.xml                 → sitemap SEO
/llms.txt                    → contexte GEO anglais (pour LLMs)
/llms-fr.txt                 → contexte GEO français (pour LLMs)
```

## Règles absolues

- **Toujours modifier FR et EN en parallèle** — le FR est la source, l'EN est traduit fidèlement
- **Jamais de `git push` sans confirmation** de Robin
- **Commits en anglais**, co-signés : `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- **Interdit** : le caractère `—` (tiret cadratin) dans tout contenu créé
- **Python** : `python` (pas `python3`) — Windows
- **Ne jamais modifier** les pages parcours/track-record depuis le contenu éditorial
- **SEO/GEO : après chaque modification ou création, vérifier systématiquement la checklist ci-dessous et signaler tout point manquant avant le commit**

## Mémoire entre sessions (`memory/`)

Le repo GitHub est **public** — ne jamais y mettre d'informations sensibles ou personnelles.

- **`CLAUDE.md`** (repo public) : toutes les règles projet, workflows, conventions. C'est ici que vont les préférences et décisions qui émergent en conversation, si elles ne sont pas sensibles.
- **`memory/`** (local, jamais pushé) : uniquement les données personnelles/privées qui ne doivent pas apparaître sur GitHub (ex : email, identité).
- **Règle** : ne jamais dupliquer dans `memory/` ce qui est déjà dans `CLAUDE.md`. Si quelque chose mérite d'être retenu entre sessions et n'est pas sensible, l'ajouter dans `CLAUDE.md`.

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

### Ordre des entrées dans `perspectives.json` — règle critique

`persp-nav.js` construit la grille en itérant le tableau **en sens inverse** (du dernier au premier).  
**Conséquence : les entrées doivent toujours être dans l'ordre chronologique — du plus ancien (index 0) au plus récent (dernier index).**  
Le dernier article du JSON est affiché en première position dans la grille.  
Si un article est ajouté ou si une date est modifiée, vérifier que l'ordre chronologique est respecté dans le tableau.

---

## Workflow — nouvel article (4 étapes)

### Étape 1 — Préparer l'input et créer le draft FR

1. Copier `article_input.example.json` en `article_input.json` et remplir tous les champs
2. Placer l'illustration dans `/assets/illus-[nom].jpg` (800x420) et l'OG image en `/assets/illus-[nom]-og.png` (1200x630)
3. Lancer le script :

```powershell
python new_article.py article_input.json
```

Le script crée `fr/perspectives/[slug-fr].html` avec `<meta name="robots" content="noindex">`.
L'article n'apparait pas dans les grilles, la home ni le sitemap — accessible uniquement par URL directe.

4. Commit + push pour déployer le draft en ligne.

### Étape 2 — Retravaille depuis l'admin

Robin édite le contenu FR via `/admin/index.html`. L'admin commite directement sur GitHub.
Après modifications via l'admin : **faire `git pull` avant de travailler en local**.

### Étapes 3 et 4 — Publication + version EN

Utiliser le skill `/publish-article` — il orchestre tout : script de publication, création EN, audit SEO/GEO, commit, IndexNow.

---

## Contenu de body_fr dans article_input.json — règles éditoriales

Le champ `body_fr` doit contenir le HTML complet du corps article (tout ce qui est dans `<div class="article-body">`), hors bloc `.article-cta` (généré automatiquement par le script).

Structure attendue :
- `<p class="lead">` — résumé de moins de 80 mots
- `<h2>` — formulés en questions ou assertions extractibles par les LLM
- `<p class="body-text">` — paragraphes
- `<div class="article-takeaways">` — bloc Points clés obligatoire
- `<p class="body-text">` — lien interne de maillage (au moins 1)

**Markup bloc Points clés** (FR) / Key takeaways (EN) :

```html
<div class="article-takeaways">
  <div class="article-takeaways-title">Points clés</div>
  <ul class="article-takeaways-list">
    <li>Point 1.</li>
    <li>Point 2.</li>
    <li>Point 3.</li>
  </ul>
</div>
```

**FAQ Schema** — à ajouter manuellement dans le `<head>` si l'article contient des questions implicites :
```json
{"@type": "FAQPage", "mainEntity": [
  {"@type": "Question", "name": "Question ?", "acceptedAnswer": {"@type": "Answer", "text": "Réponse."}}
]}
```

### 8. Commit + push (après confirmation Robin)

### 9. IndexNow ping (après push)

Utiliser le skill `/indexnow <slug-fr> <slug-en>`.

---

## Workflow — modification d'un article existant

### Via l'admin panel (`/admin/index.html`)

L'admin édite uniquement le FR et commite directement sur GitHub.
Après une modif via admin : utiliser le skill `/sync-admin <slug-fr>` — il orchestre tout : pull, traduction EN, mise à jour JSON/sitemap/llms.txt, commit, IndexNow.

---

## Admin panel — fonctionnement

`/admin/index.html` — éditeur FR uniquement, accessible via token GitHub.

- **Lit** : le fichier HTML FR depuis GitHub API
- **Édite** : titre principal (noir), sous-titre/accroche (or italique), meta description, corps de l'article
- **Commite** directement sur GitHub (branch `main`)
- **Ne traduit pas** l'EN — à faire manuellement via Claude Code après

Quand Robin dit "j'ai modifié via l'admin" : faire `git pull`, comparer FR vs EN, retraduire si nécessaire.

**Si le titre ou le sous-titre a changé via l'admin :**
1. Mettre à jour `title_fr`, `subtitle_fr`, `title_en`, `subtitle_en` dans `perspectives.json`
2. Relancer `python update_home_persp.py` (les cartes home affichent le titre depuis le JSON)
3. Mettre à jour l'entrée dans `articles-publies.md` avec le nouveau titre et une note de modification

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

## Audit SEO/GEO — checklist systématique

**A appliquer après chaque création ou modification d'article ou de page.**  
Utiliser le skill `/seo-check <slug-fr>` pour exécuter l'audit complet et signaler tout point manquant avant le commit.

Note : `robots.txt` doit autoriser explicitement — à vérifier une fois par trimestre : `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Amazonbot`, `cohere-ai`

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
