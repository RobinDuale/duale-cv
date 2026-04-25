# Dépôt duale-cv — Configuration & Déploiement

> Base de connaissances générée le 2026-04-25 — mise à jour le 2026-04-25.  
> À utiliser comme référence pour les sessions Claude Code sur ce projet.

---

## 1. Remote Git

| Paramètre | Valeur |
|-----------|--------|
| Nom du remote | `origin` |
| URL GitHub | `https://github.com/RobinDuale/duale-cv` |

---

## 2. Branches

| Branche | Rôle |
|---------|------|
| `main` | Branche principale — code de production |
| `claude/explore-repo-structure-NpVTG` | Branche de travail Claude Code |

La branche `main` est celle deployée en production via GitHub Pages.

---

## 3. Structure des dossiers à la racine

```
duale-cv/
├── fr/                        # Pages du site en français
│   ├── index.html
│   ├── a-propos.html
│   ├── parcours.html
│   ├── temoignages.html
│   ├── contact.html
│   ├── faq.html
│   ├── mentions-legales.html
│   ├── merci.html
│   └── perspectives/          # Articles de blog (FR)
│       ├── index.html
│       ├── je-suis-le-produit.html
│       ├── ia-accelerateur-organisationnel.html
│       ├── avantage-competitif-humain.html
│       ├── exit-reussi-ce-que-lacheteur-regarde-vraiment.html
│       └── migration-100-abonnement.html
│
├── en/                        # Pages du site en anglais
│   ├── index.html
│   ├── about.html
│   ├── track-record.html
│   ├── references.html
│   ├── contact.html
│   ├── faq.html
│   ├── legal-notice.html
│   ├── thank-you.html
│   └── perspectives/          # Articles de blog (EN)
│       ├── index.html
│       ├── i-am-the-product.html
│       ├── ai-organizational-accelerator.html
│       ├── competitive-edge-is-human.html
│       ├── successful-exit-what-buyers-really-look-at.html
│       └── switching-to-100-percent-subscription.html
│
├── assets/                    # Ressources statiques partagées
│   ├── css/main.css
│   ├── js/main.js
│   ├── js/persp-nav.js        # Navigation dynamique inter-articles (généré côté client)
│   ├── perspectives.json      # Source de vérité articles (slug, titre, tags — FR + EN)
│   ├── CV ROBIN DUALE (FR).pdf
│   ├── CV ROBIN DUALE (EN).pdf
│   ├── robin-duale.jpg
│   ├── favicon.svg
│   ├── preview.jpg / Prévisualisation.jpg
│   ├── epita-logo.png
│   ├── hec-paris-logo.jpg / .png
│   ├── presentation-fr.mp4
│   ├── presentation-en.mp4
│   └── illus-*.svg / .jpg / .png   # Illustrations des articles
│
├── .well-known/               # Vérification de domaine
├── index.html                 # Redirection racine vers /fr/
├── CNAME                      # Domaine personnalisé GitHub Pages
├── sitemap.xml
├── robots.txt
├── llms.txt                   # Index contenu pour LLMs (EN)
├── llms-fr.txt                # Index contenu pour LLMs (FR)
├── indexnow-ping.sh           # Script SEO manuel (Bing + Yandex)
└── A8A911547D7C17BDDBE856B293F83A46.txt   # Clé IndexNow (publique)
```

---

## 4. Domaine de production

```
cv-robin.duale.fr
```

Défini dans le fichier `CNAME` — domaine personnalisé GitHub Pages.

---

## 5. Système de déploiement

### Méthode : GitHub Pages — déploiement manuel

| Outil | Présent | Notes |
|-------|---------|-------|
| `.github/workflows/` | **Non** | Pas de GitHub Actions |
| `netlify.toml` | **Non** | Pas de Netlify |
| `package.json` | **Non** | Pas de build npm |
| `_config.yml` | **Non** | Pas de Jekyll |
| CI/CD automatique | **Non** | Aucun pipeline détecté |

**Le déploiement est entièrement manuel :**

1. Éditer les fichiers HTML/CSS/JS/assets localement
2. `git add` + `git commit` + `git push origin main`
3. GitHub Pages publie automatiquement depuis `main` après le push
4. *(Optionnel)* Lancer `bash indexnow-ping.sh` pour notifier Bing et Yandex des nouvelles URLs

### Script SEO post-déploiement

`indexnow-ping.sh` envoie une requête IndexNow à Bing et Yandex avec la liste complète des URLs du site. À exécuter manuellement depuis Git Bash après chaque push significatif.

---

## 6. Architecture du site

Site statique HTML/CSS/JS **sans framework ni générateur de site statique**.

- Pas de build step — les fichiers HTML sont directement servis
- Bilingue : `/fr/` (français) et `/en/` (anglais)
- `index.html` à la racine redirige vers `/fr/` (langue par défaut)
- CSS et JS uniques et partagés entre les deux langues (`assets/css/main.css`, `assets/js/main.js`)
- Navigation inter-articles (suivant / précédent / à lire aussi) générée dynamiquement par `assets/js/persp-nav.js` à partir de `assets/perspectives.json` — **pour ajouter un article, seul ce JSON est à modifier**

---

## 7. Ajouter un nouvel article Perspectives

1. Créer le fichier HTML dans `fr/perspectives/[slug-fr].html` et `en/perspectives/[slug-en].html`
2. Copier le `<div id="persp-nav"></div>` dans la sidebar (à la place des blocs nav hardcodés)
3. Ajouter `<script src="../../assets/js/persp-nav.js" defer></script>` après `main.js`
4. **Ajouter une entrée dans `assets/perspectives.json`** (dans l'ordre chronologique) :

```json
{
  "slug_fr": "mon-nouvel-article",
  "slug_en": "my-new-article",
  "title_fr": "Titre en français",
  "title_en": "Title in English",
  "tags_fr": "Tag1 · Tag2",
  "tags_en": "Tag1 · Tag2"
}
```

5. `git push origin main` — tous les articles existants affichent automatiquement le nouveau dans leur navigation.

---

## 8. Workflow de développement recommandé

```bash
# Travailler sur une branche feature
git checkout -b feature/ma-modification

# Tester localement (serveur statique)
python3 -m http.server 8080
# → ouvrir http://localhost:8080

# Commit et push
git add <fichiers>
git commit -m "feat: description de la modification"
git push origin feature/ma-modification

# Merger dans main pour déclencher le déploiement GitHub Pages
git checkout main
git merge feature/ma-modification
git push origin main

# SEO : notifier les moteurs de recherche
bash indexnow-ping.sh
```
