# sync-admin

Synchronise complètement le site après une modification via l'admin panel.

**Usage :** `/sync-admin <slug-fr>`  
**Exemple :** `/sync-admin autorite-dans-les-llms`

## Workflow à exécuter

L'argument `$ARGUMENTS` est le slug FR de l'article modifié.

**Si `$ARGUMENTS` est vide**, lire `assets/perspectives.json`, afficher la liste des articles publiés (hors drafts) avec leur date et titre, et demander : "Quel article veux-tu synchroniser ?" Attendre la réponse avant de continuer.

### 1. Pull

```bash
git pull origin main
```

### 2. Lire le FR mis à jour

Lire `fr/perspectives/$ARGUMENTS.html` et identifier ce qui a changé par rapport à l'EN :
- Titre principal (H1 niveau 1)
- Sous-titre (H1 niveau 2, balise `<em>`)
- Chapô (`<p class="lead">`)
- Corps de l'article (`<div class="article-body">`)
- Points clés (`.article-takeaways-list`)
- Titre CTA (`.article-cta-title`)
- Texte CTA (`.article-cta-text`)

### 3. Traduire et mettre à jour le fichier EN

Traduire fidèlement en anglais tout ce qui a changé et mettre à jour `en/perspectives/[slug-en].html`.  
**Règle absolue : aucun caractère `—` (tiret cadratin) dans la traduction.**  
Mettre à jour `dateModified` dans le Schema.org BlogPosting (FR + EN) avec la date du jour.

### 4. Si titre, sous-titre ou excerpt a changé

- Mettre à jour `assets/perspectives.json` : `title_fr`, `subtitle_fr`, `title_en`, `subtitle_en`, `excerpt_fr`, `excerpt_en`
- Vérifier que l'ordre chronologique des entrées est respecté dans le tableau (le plus récent en dernier)
- Lancer `python update_home_persp.py`

### 5. Mettre à jour les fichiers de référencement

- `sitemap.xml` : mettre à jour `lastmod` du jour sur les 2 URLs (FR + EN)
- `llms.txt` + `llms-fr.txt` : mettre à jour si le contenu a changé significativement
- `articles-publies.md` : mettre à jour `dateModified` et noter les changements

### 6. Commit automatique

```bash
git add -A
git commit -m "Sync admin: <résumé des modifications> (FR + EN)\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Le message de commit doit résumer ce qui a changé (ex: "Sync admin: update title and body autorite-dans-les-llms (FR + EN)").

### 7. Demander confirmation avant le push

Présenter un résumé de tout ce qui a été modifié et demander : **"Je pousse ?"**
