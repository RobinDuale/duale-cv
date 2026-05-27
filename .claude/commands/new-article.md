# new-article

Idéation et rédaction partielle d'un nouvel article pour la rubrique Perspectives.

**Usage :** `/new-article` ou `/new-article <sujet libre>`

## Directive de référence — style éditorial

**APPLIQUER STRICTEMENT à tout contenu produit par ce skill.**

### Audience et registre

Le texte s'adresse à des dirigeants, investisseurs, fonds, membres de board, opérateurs expérimentés. Le lecteur est supposé expérimenté, intelligent, déjà familier des sujets traités. Pas de vulgarisation, pas de sur-explication, pas de scénarisation des enjeux.

Le texte doit produire l'impression d'un auteur ayant vécu les situations qu'il décrit : intégration, gouvernance, arbitrages opérationnels, croissance, contraintes financières, relations investisseurs, organisation, exécution.

L'écriture doit évoquer une note stratégique, un mémo de réflexion, un article d'analyse économique, une observation issue de l'expérience. Jamais un contenu marketing, une publication LinkedIn, une keynote, un article de cabinet de conseil.

### Objectif éditorial

Produire un texte dense, sobre, crédible, précis, intellectuellement stable, économiquement réaliste.

Privilégier : les mécanismes, les causalités, les contraintes, les asymétries, les effets opérationnels réels, les temporalités de décision, les comportements observables.

Ne jamais chercher à inspirer, séduire, dramatiser, embarquer le lecteur, produire une impression artificielle d'intelligence.

### Style

Analytique, calme, direct, légèrement détaché, sobre, concret, structuré, opérationnel. Niveau de langage élevé sans être démonstratif.

Construction des phrases :
- Phrases courtes à moyennes
- Syntaxe simple
- Verbes concrets
- Transitions sobres
- Logique explicite
- Causalité directe

Limiter fortement : phrases longues démonstratives, phrases "signature", rythmes ternaires, formulations destinées à être citées, effets de cadence.

### Interdictions rhétoriques absolues

Ne jamais utiliser :
- « ce n'est pas..., c'est... »
- « il ne s'agit pas de..., mais de... »
- « la vraie question n'est pas... »
- « le sujet n'est pas... »
- « plus que »
- « davantage que »
- « moins... que... »
- Oppositions artificielles, fausses dialectiques, retournements rhétoriques

### Formulations interdites

Ne jamais utiliser ces formulations ni leurs variantes :

« plus que jamais » / « a l'heure ou » / « dans un monde en constante evolution » / « force est de constater » / « il convient de » / « tournant majeur » / « changer de paradigme » / « creer de la valeur » / « reinventer » / « au coeur de » / « cette dynamique » / « changer la donne » / « ce qui fait la difference » / « redefini les regles » / « il devient essentiel » / « les entreprises qui reussiront » / « saisir l'opportunite » / « accelerer » / « mutation » / « rupture » / « transformer X en Y » / « capacite a » / « vision » / « agile » / « resilient » / « scalable » / « innovation de rupture » / « penser autrement » / « repenser » / « reinventer les usages » / « nouveau paradigme » / « l'avenir appartient a »

### Interdictions de structure LLM

Eviter :
- Triades automatiques
- Listes artificiellement rythmiques
- Symétries de phrase
- Oppositions binaires
- Formulations prophétiques
- Conclusions morales implicites
- Abstractions vagues
- Généralisations définitives

Ne jamais écrire comme un modèle génératif cherchant à paraître intelligent, comme un texte optimisé pour la viralité, comme un contenu pensé pour produire des citations.

### Anthropomorphismes interdits

Ne jamais écrire :
- « le marché veut »
- « l'entreprise apprend »
- « la donnée raconte »
- « la technologie permet de rêver »
- « les organisations pensent »
- « l'écosystème évolue »

Toujours décrire des acteurs, des décisions, des contraintes, des comportements, des mécanismes observables.

### Contrainte typographique absolue

Ne jamais utiliser le tiret cadratin `—`. Remplacer par des phrases séparées, des virgules sobres, des points simples.

- **Interdit** : « Le problème est ailleurs — dans la structure même du modèle. »
- **Correct** : « Le problème se situe dans la structure du modèle. »

---

## Workflow à exécuter

### 0. Lire le contexte existant

Lire `assets/perspectives.json` pour identifier :
- Les articles déjà publiés (titre, date, angle)
- Les thèmes déjà couverts, pour éviter la redondance ou proposer une complémentarité
- La catégorie la plus récente (pour suggérer un eyebrow cohérent)

### 1. Dialogue d'idéation

Si `$ARGUMENTS` est vide, poser ces questions une par une (ne pas tout poser d'un coup) :

**Question 1** — Quel est le sujet ou l'angle de départ ? (une phrase suffit)

Attendre la réponse, puis :

**Question 2** — Quel est le contexte principal de l'article ?  
Options : SaaS B2B / Data / e-commerce / PE / LBO / gouvernance / croissance / M&A / management / autre

**Question 3** — Y a-t-il un déclencheur réel ou une tension concrète à l'origine de cet article ? (situation observée, arbitrage récent, comportement récurrent, contrainte identifiée)

**Question 4** — Durée de lecture cible ?  
Options : ~4 min (600-800 mots) / ~6 min (900-1200 mots) / ~8 min (1300-1600 mots)

Si `$ARGUMENTS` n'est pas vide, utiliser l'argument comme réponse à la Question 1 et poser les questions 2, 3, 4.

### 2. Produire le plan éditorial

Après avoir collecté les réponses, produire :

**Eyebrow** (ex : "Perspectives · SaaS · Private equity")  
**Titre principal** (noir) : assertion directe, 5-9 mots, sans tiret cadratin  
**Sous-titre** (or italique, optionnel) : accroche sobre, ou vide si le titre est autoportant  
**Meta title** : 50-60 caractères exactement (compter et indiquer le nombre)  
**Meta description** : 130-155 caractères exactement (compter et indiquer le nombre)  
**Excerpt** : 2-3 phrases sobres pour les cartes de grille et home  
**Slug FR proposé** (kebab-case, mots-clés principaux, max 6 mots)  
**Slug EN proposé** (traduction fidèle, même contrainte)  
**Nom d'illustration proposé** : `illus-[slug]-og` (ex : `illus-dilution-saas-og`)  
**Durée estimée** et **nombre de mots cible**  
**H2 proposés** (3 à 5) : formulés en questions ou assertions directes, extractibles par les LLM  

Signaler si un angle similaire existe déjà dans `perspectives.json` et proposer une différenciation.

### 3. Demander validation avant de rédiger

Afficher le plan et demander :  
**"Ce plan te convient ? Je rédige le body_fr partiel (lead + corps H2 + points clés) ?"**

Attendre confirmation avant de continuer.

### 4. Rédiger le body_fr partiel

Produire le HTML complet pour :

- `<p class="lead">` : chapô de moins de 80 mots, ton sobre, entrée directe dans le sujet
- Pour chaque H2 : `<h2>` + `<p class="body-text">` de 80-150 mots (corps de l'argument, pas de remplissage)
- `<div class="article-takeaways">` avec 4-5 points clés concrets

Ne pas rédiger l'introduction narrative, les transitions vides, les conclusions rhétoriques. Chaque paragraphe doit apporter une idée réelle.

Appliquer strictement toutes les interdictions stylistiques de la directive ci-dessus.

### 5. Produire le draft article_input.json

Après la rédaction, produire un bloc JSON complet, prêt à être copié dans `article_input.json` :

```json
{
  "slug_fr": "...",
  "slug_en": "...",
  "title_fr": "...",
  "subtitle_fr": "...",
  "title_en": "...",
  "subtitle_en": "...",
  "eyebrow_fr": "...",
  "eyebrow_en": "...",
  "date_fr": "[DATE FR — à remplir]",
  "date_en": "[DATE EN — à remplir]",
  "date_iso": "[YYYY-MM-DD — à remplir]",
  "tags_fr": "...",
  "tags_en": "...",
  "article_section": "...",
  "image_slug": "illus-...",
  "alt_fr": "...",
  "alt_en": "...",
  "meta_description_fr": "...",
  "meta_description_en": "[à traduire]",
  "og_description_fr": "...",
  "og_description_en": "[à traduire]",
  "excerpt_fr": "...",
  "excerpt_en": "[à traduire]",
  "read_time_fr": "... min de lecture",
  "read_time_en": "... min read",
  "word_count": 0,
  "keywords_fr": [],
  "keywords_en": [],
  "cta_title_fr": "",
  "cta_title_en": "",
  "body_fr": "[BODY FR RÉDIGÉ CI-DESSUS]",
  "body_en": ""
}
```

### 6. Instructions finales

Rappeler à Robin :
1. Remplir les champs `date_fr`, `date_en`, `date_iso`
2. Placer l'illustration dans `/assets/illus-[slug].jpg` (800x420) et l'OG dans `/assets/illus-[slug]-og.png` (1200x630)
3. Copier le JSON dans `article_input.json`
4. Lancer `python new_article.py article_input.json`
5. Commiter + pusher le draft pour le déployer en ligne
6. Retravail via `/admin/index.html`, puis `/publish-article` pour la publication finale
