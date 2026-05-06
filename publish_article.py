#!/usr/bin/env python
"""
publish_article.py — Publie un article FR deja en draft et met a jour tous les fichiers du site.

Usage:
    python publish_article.py article_input.json

Ce script :
  - Retire le noindex du fichier FR
  - Ajoute l'entree dans perspectives.json (ordre chronologique)
  - Lance update_home_persp.py
  - Ajoute les URLs dans sitemap.xml
  - Ajoute les entrees dans llms.txt et llms-fr.txt
  - Prepend l'entree dans articles-publies.md

Il ne cree PAS la version EN — a faire avec Claude dans la foulee.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
TODAY = date.today().strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# 1. Retire le noindex du draft FR
# ---------------------------------------------------------------------------

def remove_noindex(slug_fr):
    path = ROOT / "fr" / "perspectives" / f"{slug_fr}.html"
    if not path.exists():
        print(f"ERREUR : {path} introuvable. Lancer new_article.py d'abord.")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    noindex_tag = '  <meta name="robots" content="noindex"/>\n'

    if noindex_tag not in content:
        print(f"  noindex absent de {path.name} (deja publie ou jamais ajoute)")
        return

    content = content.replace(noindex_tag, "")
    path.write_text(content, encoding="utf-8")
    print(f"  noindex retire de fr/perspectives/{slug_fr}.html")


# ---------------------------------------------------------------------------
# 2. Ajoute l'entree dans perspectives.json
# ---------------------------------------------------------------------------

def update_perspectives_json(d):
    path = ROOT / "assets" / "perspectives.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    slug_fr = d["slug_fr"]
    if any(e.get("slug_fr") == slug_fr for e in data):
        print(f"  perspectives.json : entree '{slug_fr}' deja presente, ignoree")
        return

    entry = {
        "slug_fr": d["slug_fr"],
        "slug_en": d["slug_en"],
        "title_fr": d["title_fr"],
        "subtitle_fr": d.get("subtitle_fr", ""),
        "title_en": d["title_en"],
        "subtitle_en": d.get("subtitle_en", ""),
        "tags_fr": d["tags_fr"],
        "tags_en": d["tags_en"],
        "date_fr": d["date_fr"],
        "date_en": d["date_en"],
        "image_fr": f"/assets/{d['image_slug']}.jpg",
        "image_en": f"/assets/{d['image_slug']}.jpg",
        "alt_fr": d["alt_fr"],
        "alt_en": d["alt_en"],
        "excerpt_fr": d["excerpt_fr"],
        "excerpt_en": d["excerpt_en"],
    }
    data.append(entry)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  perspectives.json : entree ajoutee ({len(data)} articles au total)")


# ---------------------------------------------------------------------------
# 3. Regenere les cartes home
# ---------------------------------------------------------------------------

def run_update_home():
    script = ROOT / "update_home_persp.py"
    if not script.exists():
        print("  ATTENTION : update_home_persp.py introuvable, home non mise a jour")
        return
    result = subprocess.run(["python", str(script)], capture_output=True, text=True)
    if result.returncode == 0:
        print("  update_home_persp.py : home FR + EN regenerees")
    else:
        print(f"  ERREUR update_home_persp.py :\n{result.stderr}")


# ---------------------------------------------------------------------------
# 4. Sitemap
# ---------------------------------------------------------------------------

def update_sitemap(d):
    path = ROOT / "sitemap.xml"
    content = path.read_text(encoding="utf-8")

    slug_fr = d["slug_fr"]
    slug_en = d["slug_en"]

    fr_url = f"https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"
    if fr_url in content:
        print(f"  sitemap.xml : URLs deja presentes, ignorees")
        return

    fr_block = (
        f'  <url>\n'
        f'    <loc>https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html</loc>\n'
        f'    <lastmod>{TODAY}</lastmod>\n'
        f'    <changefreq>monthly</changefreq>\n'
        f'    <priority>0.80</priority>\n'
        f'    <xhtml:link rel="alternate" hreflang="en" '
        f'href="https://cv-robin.duale.fr/en/perspectives/{slug_en}.html" />\n'
        f'  </url>\n'
        f'  <url>\n'
        f'    <loc>https://cv-robin.duale.fr/en/perspectives/{slug_en}.html</loc>\n'
        f'    <lastmod>{TODAY}</lastmod>\n'
        f'    <changefreq>monthly</changefreq>\n'
        f'    <priority>0.80</priority>\n'
        f'    <xhtml:link rel="alternate" hreflang="fr" '
        f'href="https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html" />\n'
        f'  </url>\n'
    )

    content = content.replace("</urlset>", fr_block + "</urlset>")
    path.write_text(content, encoding="utf-8")
    print(f"  sitemap.xml : 2 URLs ajoutees")


# ---------------------------------------------------------------------------
# 5. llms.txt
# ---------------------------------------------------------------------------

def _full_title(title, subtitle):
    t = title.rstrip(",").rstrip(".")
    if subtitle:
        t = t + " " + subtitle.rstrip(".")
    return t


def update_llms(d):
    path = ROOT / "llms.txt"
    content = path.read_text(encoding="utf-8")

    slug_fr = d["slug_fr"]
    slug_en = d["slug_en"]

    en_entry = (
        f'- [{_full_title(d["title_en"], d.get("subtitle_en", ""))}]'
        f'(https://cv-robin.duale.fr/en/perspectives/{slug_en}.html): '
        f'{d["excerpt_en"]}'
    )
    fr_entry = (
        f'- [{_full_title(d["title_fr"], d.get("subtitle_fr", ""))}]'
        f'(https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html): '
        f'{d["excerpt_fr"]}'
    )

    if f"/en/perspectives/{slug_en}.html" in content:
        print("  llms.txt : entrees deja presentes, ignorees")
        return

    # EN entries go before "### French"
    content = content.replace("\n\n### French\n", f"\n{en_entry}\n\n### French\n")
    # FR entries go before "## Contact"
    content = content.replace("\n\n## Contact\n", f"\n{fr_entry}\n\n## Contact\n")

    path.write_text(content, encoding="utf-8")
    print("  llms.txt : 2 entrees ajoutees (EN + FR)")


# ---------------------------------------------------------------------------
# 6. llms-fr.txt
# ---------------------------------------------------------------------------

def update_llms_fr(d):
    path = ROOT / "llms-fr.txt"
    content = path.read_text(encoding="utf-8")

    slug_fr = d["slug_fr"]
    slug_en = d["slug_en"]

    fr_entry = (
        f'- [{_full_title(d["title_fr"], d.get("subtitle_fr", ""))}]'
        f'(https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html) : '
        f'{d["excerpt_fr"]}'
    )
    en_entry = (
        f'- [{_full_title(d["title_en"], d.get("subtitle_en", ""))}]'
        f'(https://cv-robin.duale.fr/en/perspectives/{slug_en}.html) : '
        f'{d["excerpt_en"]}'
    )

    if f"/fr/perspectives/{slug_fr}.html" in content:
        print("  llms-fr.txt : entrees deja presentes, ignorees")
        return

    # FR entries go before "### English"
    if "\n\n### English\n" in content:
        content = content.replace("\n\n### English\n", f"\n{fr_entry}\n\n### English\n")
    else:
        content = content.rstrip() + f"\n{fr_entry}\n"

    # EN entries: append at end of file (English section is last)
    content = content.rstrip() + f"\n{en_entry}\n"

    path.write_text(content, encoding="utf-8")
    print("  llms-fr.txt : 2 entrees ajoutees (FR + EN)")


# ---------------------------------------------------------------------------
# 7. articles-publies.md
# ---------------------------------------------------------------------------

def update_articles_publies(d):
    path = ROOT / "articles-publies.md"
    content = path.read_text(encoding="utf-8")

    slug_fr = d["slug_fr"]
    if f"/fr/perspectives/{slug_fr}.html" in content:
        print("  articles-publies.md : entree deja presente, ignoree")
        return

    schema_title_fr = _full_title(d["title_fr"], d.get("subtitle_fr", ""))
    schema_title_en = _full_title(d["title_en"], d.get("subtitle_en", ""))

    new_entry = (
        f'### {schema_title_fr}\n'
        f'\n'
        f'- **Date publiee :** {d["date_fr"]}\n'
        f'- **dateModified :** {d["date_iso"]}\n'
        f'- **Slug FR :** `fr/perspectives/{d["slug_fr"]}.html`\n'
        f'- **Slug EN :** `en/perspectives/{d["slug_en"]}.html`\n'
        f'- **Title EN :** {schema_title_en}\n'
        f'- **Categorie (eyebrow) :** {d["eyebrow_fr"]}\n'
        f'- **Tags sidebar :** {d["tags_fr"]}\n'
        f'- **Keywords schema :** {", ".join(d["keywords_fr"])}\n'
        f'- **Illustration :** `/assets/{d["image_slug"]}.jpg` / `-og.png`\n'
        f'\n'
        f'---\n'
        f'\n'
    )

    marker = "## Articles publiés\n\n---\n\n"
    if marker not in content:
        print("  ATTENTION : marqueur 'Articles publies' introuvable dans articles-publies.md")
        return

    content = content.replace(marker, marker + new_entry)
    path.write_text(content, encoding="utf-8")
    print("  articles-publies.md : entree prepend en tete de liste")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python publish_article.py article_input.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Fichier introuvable : {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        d = json.load(f)

    slug_fr = d["slug_fr"]
    slug_en = d["slug_en"]

    print(f"\nPublication de : {slug_fr}\n")

    remove_noindex(slug_fr)
    update_perspectives_json(d)
    run_update_home()
    update_sitemap(d)
    update_llms(d)
    update_llms_fr(d)
    update_articles_publies(d)

    print(f"\nFait. Prochaines etapes :")
    print(f"  1. Demander a Claude de creer en/perspectives/{slug_en}.html")
    print(f"  2. git add + commit + push")
    print(f"  3. IndexNow ping sur les 2 URLs")


if __name__ == "__main__":
    main()
