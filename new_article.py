#!/usr/bin/env python
"""
new_article.py — Crée l'article FR en mode draft (noindex, hors perspectives.json et sitemap).

Usage:
    python new_article.py article_input.json

L'article est accessible via son URL directe mais n'apparait pas dans les grilles,
la home ni le sitemap. Utiliser publish_article.py pour la mise en ligne complète.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def _schema_title(title):
    return title.rstrip(",").rstrip(".")


def _h1(title, subtitle):
    if subtitle:
        return f"{title}<br><em>{subtitle}</em>"
    return title


def _tag_spans(tags_str):
    return "\n        ".join(
        f'<span class="sidebar-article-tag">{t.strip()}</span>'
        for t in tags_str.split("·")
        if t.strip()
    )


def build_fr_html(d, draft=True):
    slug_fr = d["slug_fr"]
    slug_en = d["slug_en"]
    title_fr = d["title_fr"]
    subtitle_fr = d.get("subtitle_fr", "")
    image_slug = d["image_slug"]
    schema_title = _schema_title(title_fr)
    h1 = _h1(title_fr, subtitle_fr)
    tags = _tag_spans(d["tags_fr"])
    keywords_json = json.dumps(d["keywords_fr"], ensure_ascii=False)
    cta_title = d.get("cta_title_fr") or "Vous cherchez un CEO disponible pour ce type de mandat ?"
    noindex = '  <meta name="robots" content="noindex"/>\n' if draft else ""

    head = (
        f'<!DOCTYPE html>\n'
        f'<html lang="fr">\n'
        f'<head>\n'
        f'  <meta charset="UTF-8"/>\n'
        f'  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n'
        f'{noindex}'
        f'  <meta name="description" content="{d["meta_description_fr"]}"/>\n'
        f'  <title>{schema_title} · Perspectives · Robin Dualé</title>\n'
        f'  <meta property="og:title" content="{schema_title} · Robin Dualé"/>\n'
        f'  <meta property="og:description" content="{d["og_description_fr"]}"/>\n'
        f'  <meta property="og:url" content="https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"/>\n'
        f'  <meta property="og:type" content="article"/>\n'
        f'  <meta property="og:image" content="https://cv-robin.duale.fr/assets/{image_slug}-og.png"/>\n'
        f'  <meta property="og:image:width" content="1200"/>\n'
        f'  <meta property="og:image:height" content="630"/>\n'
        f'  <meta name="twitter:card" content="summary_large_image"/>\n'
        f'  <meta name="twitter:image" content="https://cv-robin.duale.fr/assets/{image_slug}-og.png"/>\n'
        f'  <link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg"/>\n'
        f'  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"/>\n'
        f'  <link rel="shortcut icon" href="/favicon.ico"/>\n'
        f'  <link rel="preload" href="../../assets/css/main.css" as="style"/>\n'
        f'  <link rel="stylesheet" href="../../assets/css/main.css"/>\n'
        f'  <link rel="canonical" href="https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"/>\n'
        f'  <link rel="alternate" hreflang="fr" href="https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"/>\n'
        f'  <link rel="alternate" hreflang="en" href="https://cv-robin.duale.fr/en/perspectives/{slug_en}.html"/>\n'
    )

    breadcrumb = (
        f'  <script type="application/ld+json">\n'
        f'  {{\n'
        f'    "@context": "https://schema.org",\n'
        f'    "@type": "BreadcrumbList",\n'
        f'    "itemListElement": [\n'
        f'      {{"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://cv-robin.duale.fr/fr/"}},\n'
        f'      {{"@type": "ListItem", "position": 2, "name": "Perspectives", "item": "https://cv-robin.duale.fr/fr/perspectives/"}},\n'
        f'      {{"@type": "ListItem", "position": 3, "name": "{schema_title}", "item": "https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"}}\n'
        f'    ]\n'
        f'  }}\n'
        f'  </script>\n'
    )

    blogposting = (
        f'  <script type="application/ld+json">\n'
        f'  {{\n'
        f'    "@context": "https://schema.org",\n'
        f'    "@type": "BlogPosting",\n'
        f'    "headline": "{schema_title}",\n'
        f'    "wordCount": {d["word_count"]},\n'
        f'    "articleSection": "{d["article_section"]}",\n'
        f'    "description": "{d["meta_description_fr"]}",\n'
        f'    "datePublished": "{d["date_iso"]}",\n'
        f'    "dateModified": "{d["date_iso"]}",\n'
        f'    "image": "https://cv-robin.duale.fr/assets/{image_slug}.jpg",\n'
        f'    "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"}},\n'
        f'    "author": {{"@type": "Person", "name": "Robin Dualé", "url": "https://cv-robin.duale.fr/fr/", "sameAs": "https://www.linkedin.com/in/robinduale/"}},\n'
        f'    "publisher": {{"@type": "Person", "name": "Robin Dualé"}},\n'
        f'    "url": "https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html",\n'
        f'    "inLanguage": "fr",\n'
        f'    "keywords": {keywords_json}\n'
        f'  }}\n'
        f'  </script>\n'
        f'</head>\n'
    )

    nav = (
        f'<body>\n'
        f'\n'
        f'<nav class="nav">\n'
        f'  <div class="nav-brand"><a href="/fr/" class="nav-logo">Robin Dualé</a>'
        f'<div class="nav-edu-logos">'
        f'<img src="/assets/hec-paris-logo.png" alt="HEC Paris" class="nav-edu-logo" loading="lazy"/>'
        f'<img src="/assets/epita-logo.png" alt="EPITA" class="nav-edu-logo" loading="lazy"/>'
        f'</div></div>\n'
        f'  <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false">'
        f'<span></span><span></span><span></span></button>\n'
        f'  <div class="nav-links" id="nav-links">\n'
        f'    <a class="nav-link" href="/fr/">Accueil</a>\n'
        f'    <a class="nav-link" href="/fr/a-propos.html">À propos</a>\n'
        f'    <a class="nav-link" href="/fr/parcours.html">Parcours</a>\n'
        f'    <a class="nav-link" href="/fr/temoignages.html">Témoignages</a>\n'
        f'    <a class="nav-link active" href="/fr/perspectives/">Perspectives</a>\n'
        f'    <a class="nav-link" href="/fr/contact.html">Contact</a>\n'
        f'    <div class="nav-divider"></div>\n'
        f'    <div class="lang-switcher">\n'
        f'      <a class="lang-item" href="/fr/perspectives/{slug_fr}.html">\n'
        f'        <div class="lang-dot active"></div>\n'
        f'        <span class="lang-btn active">FR</span>\n'
        f'      </a>\n'
        f'      <a class="lang-item" href="/en/perspectives/{slug_en}.html">\n'
        f'        <div class="lang-dot"></div>\n'
        f'        <span class="lang-btn">EN</span>\n'
        f'      </a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</nav>\n'
    )

    page_header = (
        f'\n'
        f'<div class="page-header">\n'
        f'  <p class="page-eyebrow">{d["eyebrow_fr"]}</p>\n'
        f'  <h1 class="page-title">{h1}</h1>\n'
        f'</div>\n'
    )

    main_col = (
        f'\n'
        f'<div class="two-col">\n'
        f'  <div class="main-col">\n'
        f'    <div class="article-illus">'
        f'<img src="/assets/{image_slug}.jpg" alt="{d["alt_fr"]}" class="article-illus-img" '
        f'width="800" height="420" loading="lazy"/></div>\n'
        f'    <div class="article-meta">\n'
        f'      <span>{d["date_fr"]}</span>\n'
        f'      <span class="article-meta-sep">·</span>\n'
        f'      <span>{d["read_time_fr"]}</span>\n'
        f'    </div>\n'
        f'\n'
        f'    <div class="article-body">\n'
        f'{d["body_fr"]}\n'
        f'\n'
        f'      <div class="article-cta">\n'
        f'        <div class="article-cta-title">{cta_title}</div>\n'
        f'        <p class="article-cta-text">Je suis disponible pour un mandat de CEO ou Directeur Général dans une entreprise B2B SaaS, BtoC, Data, IA ou e-commerce de 10 à 100 M€. Si vous conduisez une recherche ou souhaitez échanger sur ces enjeux, je suis joignable directement.</p>\n'
        f'        <div class="article-cta-links">\n'
        f'          <a class="btn-gold" href="/fr/contact.html">Me contacter</a>\n'
        f'          <a class="btn-outline" href="https://linkedin.com/in/robinduale" target="_blank">LinkedIn</a>\n'
        f'        </div>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </div>\n'
    )

    side_col = (
        f'\n'
        f'  <div class="side-col">\n'
        f'    <a class="sidebar-back" href="/fr/perspectives/">← Retour aux Perspectives</a>\n'
        f'\n'
        f'    <div class="sidebar-section">\n'
        f'      <div class="sidebar-article-date">{d["date_fr"]}</div>\n'
        f'      <div style="margin-bottom:8px">\n'
        f'        {tags}\n'
        f'      </div>\n'
        f'      <p class="sidebar-text">{d["read_time_fr"]}</p>\n'
        f'    </div>\n'
        f'\n'
        f'    <div id="persp-nav"></div>\n'
        f'    <div class="sidebar-section">\n'
        f'      <div class="sidebar-title">Robin Dualé</div>\n'
        f'      <p class="sidebar-text">CEO et Directeur Général, 18 ans en B2B, BtoC, SaaS, Data et e-commerce. Disponible pour un nouveau mandat.</p>\n'
        f'      <a class="btn-outline" href="/fr/contact.html" style="margin-top:12px;display:inline-block">Me contacter</a>\n'
        f'      <a class="btn-outline" href="https://www.linkedin.com/in/robinduale/" target="_blank" style="margin-top:8px;display:inline-block">LinkedIn</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</div>\n'
    )

    footer = (
        f'\n'
        f'<footer class="footer">\n'
        f'  <span class="footer-name">© 2026 Robin Dualé · duale.fr</span>\n'
        f'  <div class="footer-links">\n'
        f'    <a class="footer-link" href="https://linkedin.com/in/robinduale" target="_blank">LinkedIn</a>\n'
        f'    <a class="footer-link" href="mailto:robin@duale.fr">robin@duale.fr</a>\n'
        f'    <a class="footer-link" href="/fr/faq.html">FAQ</a>\n'
        f'    <a class="footer-link" href="/fr/mentions-legales.html">Mentions légales</a>\n'
        f'  </div>\n'
        f'</footer>\n'
        f'\n'
        f'<script src="../../assets/js/main.js"></script>\n'
        f'<script src="../../assets/js/persp-nav.js" defer></script>\n'
        f'<div id="cookie-banner" class="cookie-banner" style="display:none">\n'
        f'  <p class="cookie-text">Ce site utilise Google Analytics pour mesurer son audience. Acceptez-vous le dépôt de cookies analytiques ?</p>\n'
        f'  <div class="cookie-actions">\n'
        f'    <button class="cookie-btn-accept" onclick="acceptCookies()">Accepter</button>\n'
        f'    <button class="cookie-btn-refuse" onclick="refuseCookies()">Refuser</button>\n'
        f'  </div>\n'
        f'</div>\n'
        f'</body>\n'
        f'</html>\n'
    )

    return head + breadcrumb + blogposting + nav + page_header + main_col + side_col + footer


def main():
    if len(sys.argv) < 2:
        print("Usage: python new_article.py article_input.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Fichier introuvable : {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        d = json.load(f)

    slug_fr = d["slug_fr"]
    out_path = ROOT / "fr" / "perspectives" / f"{slug_fr}.html"

    if out_path.exists():
        print(f"ATTENTION : {out_path} existe deja. Ecraser ? (o/n) ", end="")
        if input().strip().lower() != "o":
            print("Annule.")
            sys.exit(0)

    html = build_fr_html(d, draft=True)
    out_path.write_text(html, encoding="utf-8")

    print(f"\nDraft cree : fr/perspectives/{slug_fr}.html")
    print(f"URL directe : https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html")
    print("\nProchaines etapes :")
    print("  1. git add + commit + push pour deployer le draft")
    print("  2. Retravaille l'article depuis l'admin")
    print("  3. python publish_article.py article_input.json pour la mise en ligne complete")


if __name__ == "__main__":
    main()
