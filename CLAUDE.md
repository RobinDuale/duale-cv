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

- **Mise à jour de CLAUDE.md après chaque problème rencontré** — si un bug, une erreur de contenu ou un problème SEO/GEO est détecté et corrigé en session, ajouter immédiatement dans CLAUDE.md une règle précise pour empêcher la récurrence : description du problème, cause, règle à respecter, vérification à faire. Ce fichier est la mémoire opérationnelle du projet — il doit grandir à chaque session.
- **Toujours modifier FR et EN en parallèle** — le FR est la source, l'EN est traduit fidèlement
- **Jamais de `git push` sans confirmation** de Robin
- **Commits en anglais**, co-signés : `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- **Interdit** : le caractère `—` (tiret cadratin) dans tout contenu créé
- **Noms de fichiers assets** : toujours en minuscules, tirets uniquement — jamais d'espaces, underscores ou majuscules (ex : `illus-mon-image.jpg`, pas `Mon Image.jpg` ni `mon_image.jpg`). Un espace dans un nom de fichier casse l'URL et provoque des images brisées en production.
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

## Worktree — synchronisation après chaque commit

**Toutes les sessions Claude Code s'exécutent dans un worktree** (`…/.claude/worktrees/<nom>/`) sur une branche séparée. Les commits sont faits sur `main` dans le répertoire principal. Le worktree ne reçoit pas ces changements automatiquement — le serveur local (port 3456) sert depuis le worktree et n'affichera pas les modifications tant que la sync n'est pas faite.

**Après chaque commit sur `main`, exécuter systématiquement dans le worktree :**

```bash
cd "C:\Users\robin\ClaudeDevRepo\duale-cv\.claude\worktrees\<nom-worktree>"
git stash   # si CLAUDE.md a des modifications locales non commitées
git merge main --no-edit
git stash pop   # si stash effectué
```

**Vérification** : après la sync, `grep "nouveau contenu" fr/index.html` dans le worktree doit retourner un résultat.

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

Le script crée deux choses :
- `fr/perspectives/[slug-fr].html` avec `<meta name="robots" content="noindex">`
- Une entrée `"draft": true` dans `perspectives.json` (en dernière position, ordre chronologique)

L'entrée draft est visible dans l'admin panel (badge "Brouillon") mais filtrée partout ailleurs : grilles, home, sitemap, navigation prev/next. `persp-nav.js` exclut systématiquement les entrées `draft: true`.

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

### Dates Schema.org — format obligatoire avec timezone

Toutes les dates dans les blocs `<script type="application/ld+json">` doivent être au format **ISO 8601 complet avec timezone**, sans quoi Google Search Console remonte des erreurs de validation :

```
✅  "datePublished": "2026-04-08T00:00:00+02:00"
✅  "dateModified":  "2026-05-05T00:00:00+02:00"
✅  "uploadDate":    "2026-03-07T00:00:00+01:00"
❌  "datePublished": "2026-04-08"   ← format trop court, rejeté par GSC
```

Règle timezone :
- Heure d'hiver (nov–mars) : `+01:00`
- Heure d'été (avr–oct) : `+02:00`

S'applique à tous les types Schema : `BlogPosting`, `ProfilePage`, `VideoObject`, etc.  
**Vérifier systématiquement ce format lors de tout ajout ou modification de date dans un bloc JSON-LD.**

### og:locale, og:image:alt, og:image:width/height — obligatoires sur tous les articles

Chaque article doit avoir dans son `<head>` :
```html
<meta property="og:locale" content="fr_FR"/>     <!-- ou en_US pour EN -->
<meta property="og:image" content="https://cv-robin.duale.fr/assets/[slug]-og.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="[alt text de l'illustration article]"/>
```

Règle image OG : utiliser l'image `[slug]-og.jpg/png` (1200×630). Si elle n'existe pas encore, utiliser l'illustration article (800×420) et corriger les dimensions déclarées. Une image OG en 404 est la cause principale d'un blocage Bing "has issues preventing indexation".

### Schema.org BlogPosting — image doit être un ImageObject

Le champ `image` doit pointer vers l'image OG (1200×630) et inclure les dimensions :
```json
"image": {"@type": "ImageObject", "url": "https://cv-robin.duale.fr/assets/[slug]-og.jpg", "width": 1200, "height": 630}
```
Ne jamais laisser `"image": "https://..."` (string seul) — les validateurs Bing/Google exigent un `ImageObject` avec dimensions ≥ 1200px de large.

### HTML valide dans les articles — interdiction `<p><ul>`

L'admin panel peut générer du HTML invalide en wrappant des `<ul>` dans des `<p>`. Vérifier et corriger :
- `<p class="body-text"><ul>` → `<ul>`
- `<p class="body-text"></p><ul>` → `<ul>`
- `</ul></p>` → `</ul>`

### `og:site_name` + Twitter Card — obligatoires sur toutes les pages

Chaque page avec des balises OG doit avoir :
```html
<meta property="og:site_name" content="Robin Dualé"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="[titre page]"/>
<meta name="twitter:description" content="[description page]"/>
<meta name="twitter:image" content="https://cv-robin.duale.fr/assets/[slug]-og.png"/>
```

### `loading="lazy"` — interdit sur l'illustration principale d'article

L'illustration principale (`class="article-illus-img"`) ne doit **pas** avoir `loading="lazy"` : Bing ne charge pas les images lazy lors du premier passage crawler. Retirer l'attribut ou le remplacer par `loading="eager"`. Le `loading="lazy"` reste acceptable sur les petites images décoratives (logos nav, etc.).

### `<strong>` au lieu de `<b>` dans les corps d'articles

Dans le contenu éditorial (`<div class="article-body">`), utiliser `<strong>` (sémantique, lu par les crawlers) plutôt que `<b>` (purement stylistique). Remplacer `<b>` par `<strong>` et `</b>` par `</strong>` à la création et lors de toute modification.

### `rel="noopener noreferrer"` — obligatoire sur tous les `target="_blank"`

Tout lien externe ouvrant un nouvel onglet doit avoir `rel="noopener noreferrer"` :
```html
<a href="https://..." target="_blank" rel="noopener noreferrer">...</a>
```
Signal qualité pour Bing/Google, et bonne pratique sécurité. À vérifier systématiquement sur tout lien ajouté.

### `<noscript>` dans `#persp-nav` — obligatoire sur tous les articles

La sidebar "À lire aussi" est 100% JS-rendered. Pour les crawlers sans JS, ajouter un fallback statique :
```html
<!-- FR -->
<div id="persp-nav"><noscript><a href="/fr/perspectives/">← Retour aux Perspectives</a></noscript></div>
<!-- EN -->
<div id="persp-nav"><noscript><a href="/en/perspectives/">← Back to Perspectives</a></noscript></div>
```
Le JS remplace le contenu du div quand il s'exécute — le noscript n'interfère pas avec le rendu normal.

### `isPartOf` Blog + `publisher` enrichi — obligatoires dans chaque BlogPosting

Chaque article (FR et EN) doit avoir dans son schema `BlogPosting` :

```json
"publisher": {"@type": "Person", "name": "Robin Dualé", "url": "https://cv-robin.duale.fr/fr/", "sameAs": "https://www.linkedin.com/in/robinduale/"},
"isPartOf": {"@type": "Blog", "url": "https://cv-robin.duale.fr/fr/perspectives/"}
```

Pour les articles EN, adapter les URLs :
```json
"publisher": {"@type": "Person", "name": "Robin Dualé", "url": "https://cv-robin.duale.fr/en/", "sameAs": "https://www.linkedin.com/in/robinduale/?locale=en-US"},
"isPartOf": {"@type": "Blog", "url": "https://cv-robin.duale.fr/en/perspectives/"}
```

- `new_article.py` génère déjà ces deux champs correctement pour le FR.
- Lors de la création manuelle de l'article EN (dans le workflow `/publish-article`), inclure ces champs EN.
- **Cause historique** : les articles n'avaient pas `isPartOf` et le `publisher` était trop pauvre — corrigés en mai 2026.

### `subjectOf` Blog dans le schema Person des home pages — à maintenir

Les fichiers `fr/index.html` et `en/index.html` ont un champ `"subjectOf"` dans le schema `Person` (dans `mainEntity`) qui lie le profil au Blog Perspectives. Ne pas supprimer ce champ lors de modifications du schema.

### `blogPost` array dans le schema Blog des index Perspectives — à maintenir à jour

Les fichiers `fr/perspectives/index.html` et `en/perspectives/index.html` ont un schema `Blog` avec un tableau `blogPost` listant tous les articles. **À chaque publication d'un nouvel article**, ajouter l'entrée dans les deux fichiers :

```json
{"@type": "BlogPosting", "headline": "[titre article]", "url": "https://cv-robin.duale.fr/fr/perspectives/[slug-fr].html"}
```

Et en EN :
```json
{"@type": "BlogPosting", "headline": "[title EN]", "url": "https://cv-robin.duale.fr/en/perspectives/[slug-en].html"}
```

Vérifier que l'ordre est cohérent (du plus ancien au plus récent). Ce tableau est le signal principal pour que Bing/Copilot comprenne que Robin Dualé est l'auteur d'un corpus d'articles structuré.

### Fallback statique `<ul>` dans les index Perspectives — à maintenir à jour

`persp-nav.js` génère la grille d'articles en JS. Pour que Bing puisse découvrir les articles sans exécuter JS, les fichiers `fr/perspectives/index.html` et `en/perspectives/index.html` contiennent une liste statique `<ul>` à l'intérieur de `#persp-grid`.

**À chaque publication d'un nouvel article**, ajouter le lien dans les deux listes :
```html
<!-- dans fr/perspectives/index.html -->
<li><a href="/fr/perspectives/[slug-fr].html">[titre FR]</a></li>
<!-- dans en/perspectives/index.html -->
<li><a href="/en/perspectives/[slug-en].html">[titre EN]</a></li>
```
Si ce fallback est absent ou incomplet, Bing peut ne pas découvrir les nouveaux articles lors du premier crawl.

---

### hreflang x-default — obligatoire sur toutes les pages

Chaque page bilingue (FR + EN) doit avoir un `hreflang="x-default"` pointant vers la version EN (fallback international). S'applique au `<head>` HTML **et** au bloc `<url>` du sitemap.

**Dans le `<head>` HTML** (après les liens hreflang fr/en) :
```html
<link rel="alternate" hreflang="fr" href="https://cv-robin.duale.fr/fr/perspectives/slug-fr.html"/>
<link rel="alternate" hreflang="en" href="https://cv-robin.duale.fr/en/perspectives/slug-en.html"/>
<link rel="alternate" hreflang="x-default" href="https://cv-robin.duale.fr/en/perspectives/slug-en.html"/>
```

**Dans `sitemap.xml`** (après `<loc>`) :
```xml
<xhtml:link rel="alternate" hreflang="x-default" href="https://cv-robin.duale.fr/en/perspectives/slug-en.html" />
<xhtml:link rel="alternate" hreflang="fr" href="https://cv-robin.duale.fr/fr/perspectives/slug-fr.html" />
<xhtml:link rel="alternate" hreflang="en" href="https://cv-robin.duale.fr/en/perspectives/slug-en.html" />
```

Les scripts `new_article.py` et `publish_article.py` doivent générer ces trois liens. Vérifier systématiquement lors de tout nouvel article ou nouvelle page.

Note : `robots.txt` doit autoriser explicitement — à vérifier une fois par trimestre : `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Amazonbot`, `cohere-ai`

### Meta description — longueur maximale 155 caractères

Google tronque les meta descriptions au-delà de ~155 caractères dans les SERPs. Au-delà de 160 c'est systématiquement coupé.

- **Règle** : toute meta description doit faire entre 130 et 155 caractères.
- **Vérification** : compter les caractères avant de valider. En Python : `len("texte")`.
- **S'applique à** : toutes les pages, articles et pages de positionnement, FR et EN.
- **Cause historique** : les pages Home FR (186 car.) et EN (184 car.) dépassaient la limite — corrigées en mai 2026.

### Title tag — longueur maximale 65 caractères

Google tronque les title tags au-delà de ~65 caractères dans les SERPs (environ 600px de large).

- **Règle** : tout title tag doit faire entre 50 et 65 caractères.
- **Vérification** : compter les caractères avant de valider.
- **S'applique à** : toutes les pages, articles et pages de positionnement, FR et EN.
- **Cause historique** : `fr/ceo-transformation-croissance-b2b-saas-data.html` avait un title à 74 caractères — corrigé en mai 2026.
- **Rappel** : quand le title change, mettre à jour `og:title` en conséquence sur la même page.

### robots.txt — ne jamais bloquer `/assets/*.mp4`

Le fichier `robots.txt` ne doit pas contenir `Disallow: /assets/*.mp4`. Les vidéos `presentation-fr.mp4` et `presentation-en.mp4` sont référencées dans les schémas `VideoObject` — si Google/Bing ne peut pas les crawler, les schémas ne peuvent jamais être validés.

- **Règle** : `Allow: /assets/*.mp4` (ou absence de règle spécifique sur les mp4).
- **Vérification** : après toute modification de `robots.txt`, contrôler qu'aucune règle ne bloque `/assets/`.
- **Cause historique** : `Disallow: /assets/*.mp4` avait été ajouté par erreur — corrigé en mai 2026.

### Liens de sidebar — pas de lien mort, pas de doublon

Les blocs `.geo-list` dans les sidebars des pages de positionnement peuvent contenir des liens morts (vers des pages supprimées ou jamais créées) ou des doublons (même href répété deux fois).

- **Règle** : après toute création, renommage ou suppression de page, grep le slug concerné dans tous les fichiers HTML et corriger les références cassées.
- **Vérification** : `grep -r "slug-supprime" fr/ en/` — toute occurrence dans un `href` doit être remplacée.
- **Pas de doublon** : dans un `.geo-list`, chaque lien doit pointer vers une URL unique. Vérifier visuellement les sidebars lors de tout ajout de lien.
- **FR et EN indépendants** : un lien mort en FR n'implique pas forcément le même problème en EN (les slugs sont différents). Vérifier les deux versions séparément.
- **Cause historique** : `ia-strategie-saas-b2b.html` (page jamais créée) était référencée dans 2 sidebars FR ; un doublon existait dans `fr/ceo-saas-lbo.html` — corrigés en mai 2026.

---

## Positionnement éditorial

- **Secteurs** : BtoC ou B2B, SaaS, Data, e-commerce, IA
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
