"""
update_home_persp.py
--------------------
Lit assets/perspectives.json, extrait les 3 articles les plus recents
et met a jour le bloc persp-teaser-grid dans fr/index.html et en/index.html
avec du HTML statique pur.

Usage : python update_home_persp.py
A executer avant chaque commit lors de l'ajout d'un nouvel article.
"""

import json
import re
from datetime import datetime
from pathlib import Path

ROOT      = Path(__file__).parent
JSON_PATH = ROOT / "assets" / "perspectives.json"
FR_HOME   = ROOT / "fr" / "index.html"
EN_HOME   = ROOT / "en" / "index.html"


def parse_date(article):
    """Convertit la date EN en objet datetime pour tri."""
    try:
        return datetime.strptime(article["date_en"], "%b %d, %Y")
    except ValueError:
        return datetime.min


def build_card_fr(article):
    return (
        f'      <a class="persp-teaser-card" href="/fr/perspectives/{article["slug_fr"]}.html">\n'
        f'        <div class="persp-card-date">{article["date_fr"]}</div>\n'
        f'        <div class="persp-card-title">{article["title_fr"]}</div>\n'
        f'        <p class="persp-card-excerpt">{article["excerpt_fr"]}</p>\n'
        f'      </a>'
    )


def build_card_en(article):
    return (
        f'      <a class="persp-teaser-card" href="/en/perspectives/{article["slug_en"]}.html">\n'
        f'        <div class="persp-card-date">{article["date_en"]}</div>\n'
        f'        <div class="persp-card-title">{article["title_en"]}</div>\n'
        f'        <p class="persp-card-excerpt">{article["excerpt_en"]}</p>\n'
        f'      </a>'
    )


def update_home(html_path, cards_html):
    content = html_path.read_text(encoding="utf-8")
    pattern = r'(<div class="persp-teaser-grid">)(.*?)(    </div>)'
    replacement = f'\\1\n{cards_html}\n    \\3'
    new_content, n = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if n == 0:
        print(f"  [!] Bloc persp-teaser-grid introuvable dans {html_path.name} — aucune modification.")
    elif new_content == content:
        print(f"  [=] {html_path.name} : deja a jour, rien a faire.")
    else:
        html_path.write_text(new_content, encoding="utf-8")
        print(f"  [OK] {html_path.name} mis a jour.")


def en_file_exists(article):
    """Retourne True si le fichier EN de l'article existe deja sur le disque."""
    en_path = ROOT / "en" / "perspectives" / f"{article['slug_en']}.html"
    return en_path.exists()


def main():
    articles = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    top3 = sorted(articles, key=parse_date, reverse=True)[:3]

    print("3 articles selectionnes (les plus recents) :")
    for a in top3:
        print(f"  {a['date_en']:15}  {a['title_en']}")

    # Home FR : toujours les 3 plus recents
    print()
    update_home(FR_HOME, "\n".join(build_card_fr(a) for a in top3))

    # Home EN : uniquement les articles dont le fichier EN existe
    top3_en = [a for a in top3 if en_file_exists(a)]
    skipped  = [a for a in top3 if not en_file_exists(a)]

    if skipped:
        print("  [INFO] Articles ignores sur home EN (fichier EN absent) :")
        for a in skipped:
            print(f"         - {a['slug_en']}.html")

    if top3_en:
        update_home(EN_HOME, "\n".join(build_card_en(a) for a in top3_en))
    else:
        print("  [!] Aucun article EN disponible — home EN non modifiee.")

    print("\nTermine. Verifiez visuellement fr/ et en/ avant de commiter.")


if __name__ == "__main__":
    main()
