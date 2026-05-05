# Articles publiés — Perspectives · cv-robin.duale.fr

Mettre à jour ce fichier après chaque publication.  
Ajouter la nouvelle entrée en haut de la liste (ordre antéchronologique).

---

## Structure technique de référence

Ces conventions sont extraites des fichiers HTML existants.  
Tout nouvel article doit les respecter scrupuleusement.

### Chemins et nommage des fichiers

- FR : `fr/perspectives/[slug-fr].html`
- EN : `en/perspectives/[slug-en].html`
- Assets CSS : `../../assets/css/main.css`
- Assets JS : `../../assets/js/main.js`
- Favicon : `../../assets/favicon.svg`
- Illustrations : `/assets/illus-[nom].svg` ou `/assets/illus-[nom].jpg`
- OG image : `/assets/illus-[nom]-og.png` (1200×630px)

### Classes CSS clés à utiliser

| Élément | Classe / balise |
|---------|----------------|
| Conteneur article | `<div class="two-col">` avec `<div class="main-col">` et `<div class="side-col">` |
| Eyebrow (breadcrumb) | `<p class="page-eyebrow">` |
| Titre H1 | `<h1 class="page-title">` — saut de ligne avec `<br>` + italique sur sous-titre avec `<em>` |
| Illustration | `<div class="article-illus"><img class="article-illus-img" width="800" height="420">` |
| Date + lecture | `<div class="article-meta">` avec `<span class="article-meta-sep">·</span>` |
| Corps | `<div class="article-body">` |
| Chapô | `<p class="lead">` |
| Paragraphes | `<p class="body-text">` |
| CTA | `<div class="article-cta">` avec `<div class="article-cta-title">`, `<p class="article-cta-text">`, `<div class="article-cta-links">` |
| Boutons CTA | `<a class="btn-gold">` (principal) et `<a class="btn-outline">` (LinkedIn) |
| Note/callout | `<div class="callout-note">` (voir article exit pour le style inline exact) |
| Tags sidebar | `<span class="sidebar-article-tag">` |
| Navigation sidebar | `<div class="sidebar-title">` + `<a class="persp-card-link">` |
| Bouton retour | `<a class="sidebar-back" href="/fr/perspectives/">← Retour aux Perspectives</a>` |

### Schema.org (obligatoire dans chaque article)

Deux blocs `<script type="application/ld+json">` :

- **BreadcrumbList** — 3 niveaux : Accueil > Perspectives > [Titre article]
- **BlogPosting** — champs : `headline`, `wordCount`, `articleSection`, `description`, `datePublished`, `dateModified`, `image`, `mainEntityOfPage`, `author`, `publisher`, `url`, `inLanguage`, `keywords`

### Balises meta obligatoires

```html
<meta name="description" content="..."/>
<title>[Titre court] · Robin Dualé</title>
<meta property="og:title" content="..."/>
<meta property="og:description" content="..."/>
<meta property="og:url" content="https://cv-robin.duale.fr/fr/perspectives/[slug].html"/>
<meta property="og:type" content="article"/>
<meta property="og:image" content="https://cv-robin.duale.fr/assets/illus-[nom]-og.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="..."/>
<link rel="canonical" href="..."/>
<link rel="alternate" hreflang="fr" href="..."/>
<link rel="alternate" hreflang="en" href="..."/>
```

### Lang switcher (dans la nav)

```html
<div class="lang-switcher">
  <a class="lang-item" href="/fr/perspectives/[slug-fr].html">
    <div class="lang-dot active"></div>
    <span class="lang-btn active">FR</span>
  </a>
  <a class="lang-item" href="/en/perspectives/[slug-en].html">
    <div class="lang-dot"></div>
    <span class="lang-btn">EN</span>
  </a>
</div>
```

### Lien Perspectives actif dans la nav

Utiliser `class="nav-link active"` sur le lien Perspectives pour tous les nouveaux articles.

---

## Articles publiés

---

### Construire maintenant son autorité dans les LLMs, est-ce une question de survie ?

- **Date publiée :** 6 mai 2026
- **dateModified :** 2026-05-06
- **Catégorie (eyebrow) :** Perspectives · SEO & GEO · Visibilité
- **Tags sidebar :** SEO · GEO · IA
- **Keywords schema :** LLM, autorité thématique, SEO, GEO, PME, visibilité IA, référencement, ChatGPT, Claude, Perplexity
- **Temps de lecture :** 5 min
- **wordCount schema :** 950
- **Slug FR :** `autorite-dans-les-llms`
- **Slug EN :** `llm-authority`
- **Illustration :** `illus-llms.png` (FR) / `illus-llms-en.png` (EN) / OG : `illus-llms-og.png` / `illus-llms-en-og.png`
- **articleSection :** SEO & GEO · Visibilité
- **Angle :** Signal personnel (site indexé dans les LLMs en un mois sans budget) comme point de départ d'une réflexion stratégique pour les PME — autorité thématique et fenêtre du premier entrant
- **Structure :** 3 H2 + FAQ Schema (3 Q/R) + Points clés + CTA "Échanger sur ces sujets"
- **Sujets couverts :** autorité thématique, GEO (Generative Engine Optimization), visibilité IA, SEO vs LLMs, prime au premier entrant, stratégie éditoriale PME, e-commerce spécialisé vs généraliste

---

### Savoir transformer la pression en ambition, est-ce vraiment ce qui fait la différence ?

- **Date publiée :** 2 mai 2026
- **dateModified :** 2026-05-04 (corrections typo FR : "focussant" → "focalisant", "l'intension" → "l'intention" ; H1 split deux niveaux ; retraduction EN)
- **Catégorie (eyebrow) :** Perspectives · Leadership & Gouvernance
- **Tags sidebar :** Leadership · Gouvernance · Private equity
- **Keywords schema :** leadership, gouvernance, private equity, CEO, ambition, pression, transformation, management, croissance, équipe
- **Temps de lecture :** 6 min
- **wordCount schema :** 950
- **Slug FR :** `transformer-la-pression-en-ambition`
- **Slug EN :** `turning-pressure-into-ambition`
- **Illustration :** `illus-pression-ambition.jpg` (JPG) / OG : `illus-pression-ambition-og.png`
- **articleSection :** Leadership & Gouvernance
- **Angle :** Question posée par un chasseur de têtes mandaté par un fonds -- transformer la pression structurelle de croissance en ambition partagée avec les équipes, sans filtrer ni lisser
- **Structure :** intro (scène entretien chasseur de têtes) + 4 H2 + CTA "Vous cherchez un CEO pour piloter une phase de croissance accélérée ?"
- **Sujets couverts :** pression PE, calibrage des objectifs, boomerang des objectifs mal calibrés, traduction stratégie fonds vers équipes, vision CEO, articulation cadre financier et opérationnel

---

### Acquisition : ce que l'acheteur sous-estime presque toujours

- **Date publiée :** 28 avril 2026
- **dateModified :** 2026-05-05 (ajout section Points clés / Key takeaways ; suppression em dash dans body FR + EN)
- **Catégorie (eyebrow) :** Perspectives · M&A & Intégration
- **Tags sidebar :** M&A · Intégration · Private equity
- **Keywords schema :** acquisition, intégration, post-acquisition, M&A, private equity, CEO, SaaS, culture, management, due diligence
- **Temps de lecture :** 6 min
- **wordCount schema :** 1100
- **Slug FR :** `acquisition-ce-que-lacheteur-sous-estime`
- **Slug EN :** `acquisition-what-buyers-almost-always-underestimate`
- **Illustration :** `illus-acquisition.jpg` (JPG) / OG : `illus-acquisition-og.jpg`
- **articleSection :** M&A & Intégration
- **Angle :** Double expérience acquéreur/acquis — les six points humains que l'acheteur sous-estime et qui font basculer l'intégration post-acquisition
- **Structure :** 6 H2 + CTA "Vous pilotez une recherche de CEO ?"
- **Sujets couverts :** intégration post-acquisition, culture d'entreprise, management d'équipe, retention des talents, communication, due diligence humaine

---

### Exit réussi : ce que l'acheteur regarde vraiment

- **Date publiée :** 24 avril 2026
- **dateModified :** 2026-05-05 (ajout section Points clés / Key takeaways FR + EN)
- **Catégorie (eyebrow) :** Perspectives · M&A & Private Equity
- **Tags sidebar :** M&A · Private equity · SaaS
- **Keywords schema :** exit, M&A, private equity, ARR, NRR, due diligence, CEO, SaaS, valorisation, data room
- **Temps de lecture :** 7 min
- **wordCount schema :** 950
- **Slug FR :** `exit-reussi-ce-que-lacheteur-regarde-vraiment`
- **Slug EN :** `successful-exit-what-buyers-really-look-at`
- **Illustration :** `illus-exits-steps.jpg` (JPG) / OG : `illus-exits-og.png`
- **articleSection :** M&A & Private Equity
- **Angle :** Double casquette vendeur/acheteur — les 5 signaux qui font basculer la due diligence
- **Structure :** 6 H2 + callout-note + CTA "Vous pilotez une recherche de CEO ?"
- **Sujets couverts :** due diligence, ARR, NRR, management package, stratégie IA en contexte exit, préparation à la cession, dashboards KPI

---

### Passer au tout-abonnement

- **Date publiée :** 17 avril 2026
- **dateModified :** 2026-05-05 (ajout section Points clés / Key takeaways FR + EN)
- **Catégorie (eyebrow) :** Perspectives · SaaS & Transformation
- **Tags sidebar :** SaaS · Abonnement · Transformation
- **Keywords schema :** SaaS, abonnement, ARR, transformation, CEO, private equity, churn, modèle économique
- **Temps de lecture :** 5 min
- **wordCount schema :** 640
- **Slug FR :** `migration-100-abonnement`
- **Slug EN :** `switching-to-100-percent-subscription`
- **Illustration :** `illus-subscription.svg` / OG : `illus-subscription-og.png`
- **articleSection :** SaaS & Transformation
- **Angle :** Deux migrations conduites — le frein client qui disparaît quand on ouvre les données de consommation réelle
- **Structure :** 4 H2 + CTA "Vous avez un modèle mixte à faire évoluer ?"
- **Sujets couverts :** migration abonnement, modèle mixte, ARR, NRR, gestion du changement client, valorisation, churn

---

### L'avantage compétitif sera profondément humain

- **Date publiée :** 13 avril 2026
- **dateModified :** 2026-05-05 (ajout section Points clés / Key takeaways FR + EN)
- **Catégorie (eyebrow) :** Perspectives · IA & Leadership
- **Tags sidebar :** IA · Leadership · Responsabilité
- **Keywords schema :** IA, leadership, transformation, CEO, humain, responsabilité, avantage compétitif
- **Temps de lecture :** 5 min
- **wordCount schema :** 520
- **Slug FR :** `avantage-competitif-humain`
- **Slug EN :** `competitive-edge-is-human`
- **Illustration :** `illus-human-edge.svg` / OG : `illus-human-edge-og.png`
- **articleSection :** IA & Leadership
- **Angle :** Le rapport mondial sur le bonheur comme signal d'alerte — rôle du dirigeant pour conduire la transformation IA sans imposer une pression supplémentaire à une génération déjà fragilisée
- **Structure :** 4 H2 + source externe (lien franceinfo) + CTA "Ces sujets vous concernent ?"
- **Sujets couverts :** IA et travail, bien-être, fragilisation générationnelle, soft skills, leadership humain, responsabilité dirigeant

---

### Le gain de productivité n'est plus une promesse

- **Date publiée :** 10 avril 2026
- **dateModified :** 2026-05-05 (ajout section Points clés / Key takeaways FR + EN ; suppression em dash dans body EN)
- **Catégorie (eyebrow) :** Perspectives · IA · Transformation organisationnelle
- **Tags sidebar :** IA · Leadership · Transformation
- **Keywords schema :** IA, transformation organisationnelle, CEO, productivité, leadership, B2B SaaS
- **Temps de lecture :** 5 min
- **wordCount schema :** 560
- **Slug FR :** `ia-accelerateur-organisationnel`
- **Slug EN :** `ai-organizational-accelerator`
- **Illustration :** `illus-productivity.svg` / OG : `illus-productivity-og.png`
- **articleSection :** IA & Transformation organisationnelle
- **Angle :** Suite d'un post LinkedIn viral (6 000 vues, 37 commentaires) — ce que la réaction révèle sur l'écart entre discours IA et expérimentation réelle en entreprise
- **Structure :** 3 H2 + CTA "Ces sujets vous concernent ?"
- **Sujets couverts :** productivité IA, adoption IA en entreprise, transformation organisationnelle, écart discours/pratique, private equity

---

### Je suis le produit

- **Date publiée :** 8 avril 2026
- **dateModified :** 2026-05-05 (ajout section Points clés / Key takeaways FR + EN ; suppression em dash dans body FR + EN)
- **Catégorie (eyebrow) :** Perspectives · IA & Personal branding
- **Tags sidebar :** IA · Personal branding
- **Keywords schema :** CEO, IA, personal branding, go-to-market, transformation digitale
- **Temps de lecture :** 4 min
- **wordCount schema :** 480
- **Slug FR :** `je-suis-le-produit`
- **Slug EN :** `i-am-the-product`
- **Illustration :** `illus-product.svg` / OG : `illus-product-og.png`
- **articleSection :** IA & Personal branding
- **Angle :** Aborder une transition de carrière comme un lancement produit — même méthode go-to-market, IA comme accélérateur de visibilité
- **Structure :** 3 H2 + CTA "Échanger sur ces sujets"
- **Sujets couverts :** personal branding dirigeant, transition CEO, création de site avec IA, Claude, HeyGen, go-to-market personnel

