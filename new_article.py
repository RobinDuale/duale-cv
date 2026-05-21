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

# ── Share bar SVGs (inline, no external lib) ──
_LI = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
_X = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.736-8.845L1.254 2.25H8.08l4.259 5.631 5.905-5.631zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'
_FB = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>'
_WA = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>'
_EM = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 7 10-7"/></svg>'
_CP = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
_PR = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>'

SHARE_TOP_FR = (
    f'    <div class="article-share">\n'
    f'      <span class="article-share-label">Partager</span>\n'
    f'      <div class="article-share-actions">\n'
    f'        <a class="article-share-btn js-share-linkedin" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur LinkedIn">{_LI}<span>LinkedIn</span></a>\n'
    f'        <a class="article-share-btn js-share-x" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur X">{_X}<span>X</span></a>\n'
    f'        <a class="article-share-btn js-share-facebook" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur Facebook">{_FB}<span>Facebook</span></a>\n'
    f'        <a class="article-share-btn js-share-whatsapp" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur WhatsApp">{_WA}<span>WhatsApp</span></a>\n'
    f'        <a class="article-share-btn js-share-email" href="#" aria-label="Envoyer par email">{_EM}<span>Email</span></a>\n'
    f'        <button class="article-share-btn js-share-copy" data-copied="Lien copié !" aria-label="Copier le lien">{_CP}<span>Copier</span></button>\n'
    f'        <button class="article-share-btn js-share-print" aria-label="Imprimer">{_PR}<span>Imprimer</span></button>\n'
    f'      </div>\n'
    f'    </div>'
)

SHARE_BOTTOM_FR = (
    f'      <div class="article-share article-share--bottom">\n'
    f'        <p class="article-share-title">Cet article vous a plu ? Partagez-le.</p>\n'
    f'        <div class="article-share-actions">\n'
    f'          <a class="article-share-btn js-share-linkedin" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur LinkedIn">{_LI}<span>LinkedIn</span></a>\n'
    f'          <a class="article-share-btn js-share-x" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur X">{_X}<span>X</span></a>\n'
    f'          <a class="article-share-btn js-share-facebook" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur Facebook">{_FB}<span>Facebook</span></a>\n'
    f'          <a class="article-share-btn js-share-whatsapp" href="#" target="_blank" rel="noopener noreferrer" aria-label="Partager sur WhatsApp">{_WA}<span>WhatsApp</span></a>\n'
    f'          <a class="article-share-btn js-share-email" href="#" aria-label="Envoyer par email">{_EM}<span>Email</span></a>\n'
    f'          <button class="article-share-btn js-share-copy" data-copied="Lien copié !" aria-label="Copier le lien">{_CP}<span>Copier</span></button>\n'
    f'          <button class="article-share-btn js-share-print" aria-label="Imprimer">{_PR}<span>Imprimer</span></button>\n'
    f'        </div>\n'
    f'      </div>'
)


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
        f'  <meta property="og:site_name" content="Robin Dualé"/>\n'
        f'  <meta property="og:locale" content="fr_FR"/>\n'
        f'  <meta property="og:image" content="https://cv-robin.duale.fr/assets/{image_slug}-og.png"/>\n'
        f'  <meta property="og:image:width" content="1200"/>\n'
        f'  <meta property="og:image:height" content="630"/>\n'
        f'  <meta property="og:image:alt" content="{d["alt_fr"]}"/>\n'
        f'  <meta name="twitter:card" content="summary_large_image"/>\n'
        f'  <meta name="twitter:title" content="{schema_title} · Robin Dualé"/>\n'
        f'  <meta name="twitter:description" content="{d["og_description_fr"]}"/>\n'
        f'  <meta name="twitter:image" content="https://cv-robin.duale.fr/assets/{image_slug}-og.png"/>\n'
        f'  <link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg"/>\n'
        f'  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"/>\n'
        f'  <link rel="shortcut icon" href="/favicon.ico"/>\n'
        f'  <link rel="preload" href="../../assets/css/main.css" as="style"/>\n'
        f'  <link rel="stylesheet" href="../../assets/css/main.css"/>\n'
        f'  <link rel="canonical" href="https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"/>\n'
        f'  <link rel="alternate" hreflang="fr" href="https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"/>\n'
        f'  <link rel="alternate" hreflang="en" href="https://cv-robin.duale.fr/en/perspectives/{slug_en}.html"/>\n'
        f'  <link rel="alternate" hreflang="x-default" href="https://cv-robin.duale.fr/en/perspectives/{slug_en}.html"/>\n'
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
        f'    "image": {{"@type": "ImageObject", "url": "https://cv-robin.duale.fr/assets/{image_slug}-og.png", "width": 1200, "height": 630}},\n'
        f'    "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html"}},\n'
        f'    "author": {{"@type": "Person", "name": "Robin Dualé", "url": "https://cv-robin.duale.fr/fr/", "sameAs": "https://www.linkedin.com/in/robinduale/"}},\n'
        f'    "publisher": {{"@type": "Person", "name": "Robin Dualé", "url": "https://cv-robin.duale.fr/fr/", "sameAs": "https://www.linkedin.com/in/robinduale/"}},\n'
        f'    "url": "https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html",\n'
        f'    "inLanguage": "fr",\n'
        f'    "isPartOf": {{"@type": "Blog", "url": "https://cv-robin.duale.fr/fr/perspectives/"}},\n'
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
        f'width="800" height="420"/></div>\n'
        f'    <div class="article-meta">\n'
        f'      <span>{d["date_fr"]}</span>\n'
        f'      <span class="article-meta-sep">·</span>\n'
        f'      <span>{d["read_time_fr"]}</span>\n'
        f'    </div>\n'
        f'\n'
        f'{SHARE_TOP_FR}\n'
        f'\n'
        f'    <div class="article-body">\n'
        f'{d["body_fr"]}\n'
        f'\n'
        f'{SHARE_BOTTOM_FR}\n'
        f'\n'
        f'      <div class="article-cta">\n'
        f'        <div class="article-cta-title">{cta_title}</div>\n'
        f'        <p class="article-cta-text">Je suis disponible pour un mandat de CEO ou Directeur Général dans une entreprise B2B SaaS, BtoC, Data, IA ou e-commerce de 10 à 100 M€. Si vous conduisez une recherche ou souhaitez échanger sur ces enjeux, je suis joignable directement.</p>\n'
        f'        <div class="article-cta-links">\n'
        f'          <a class="btn-gold" href="/fr/contact.html">Me contacter</a>\n'
        f'          <a class="btn-outline" href="https://linkedin.com/in/robinduale" target="_blank" rel="noopener noreferrer">LinkedIn</a>\n'
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
        f'    <div id="persp-nav"><noscript><a href="/fr/perspectives/">← Retour aux Perspectives</a></noscript></div>\n'
        f'    <div class="sidebar-section">\n'
        f'      <div class="sidebar-title">Robin Dualé</div>\n'
        f'      <p class="sidebar-text">CEO et Directeur Général, 18 ans en B2B, BtoC, SaaS, Data et e-commerce. Disponible pour un nouveau mandat.</p>\n'
        f'      <a class="btn-outline" href="/fr/contact.html" style="margin-top:12px;display:inline-block">Me contacter</a>\n'
        f'      <a class="btn-outline" href="https://www.linkedin.com/in/robinduale/" target="_blank" rel="noopener noreferrer" style="margin-top:8px;display:inline-block">LinkedIn</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</div>\n'
    )

    footer = (
        f'\n'
        f'<footer class="footer">\n'
        f'  <span class="footer-name">© 2026 Robin Dualé · duale.fr</span>\n'
        f'  <div class="footer-links">\n'
        f'    <a class="footer-link" href="https://linkedin.com/in/robinduale" target="_blank" rel="noopener noreferrer">LinkedIn</a>\n'
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

    # Ajoute l'entree draft dans perspectives.json pour que l'admin puisse l'editer.
    # persp-nav.js filtre les entrees draft=true : la grille et la home ne l'affichent pas.
    persp_path = ROOT / "assets" / "perspectives.json"
    with open(persp_path, encoding="utf-8") as f:
        articles = json.load(f)

    image_slug = d["image_slug"]
    already = any(a.get("slug_fr") == slug_fr for a in articles)
    if not already:
        articles.append({
            "slug_fr":    d["slug_fr"],
            "slug_en":    d["slug_en"],
            "title_fr":   d["title_fr"],
            "subtitle_fr": d.get("subtitle_fr", ""),
            "title_en":   d["title_en"],
            "subtitle_en": d.get("subtitle_en", ""),
            "tags_fr":    d["tags_fr"],
            "tags_en":    d["tags_en"],
            "date_fr":    d["date_fr"],
            "date_en":    d["date_en"],
            "image_fr":   f"/assets/{image_slug}.jpg",
            "image_en":   f"/assets/{image_slug}.jpg",
            "alt_fr":     d["alt_fr"],
            "alt_en":     d["alt_en"],
            "excerpt_fr": d["excerpt_fr"],
            "excerpt_en": d["excerpt_en"],
            "draft":      True,
        })
        with open(persp_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"  perspectives.json mis a jour (entree draft ajoutee en fin de tableau)")
    else:
        print(f"  perspectives.json : entree {slug_fr} deja presente, pas de modification")

    print(f"\nDraft cree : fr/perspectives/{slug_fr}.html")
    print(f"URL directe : https://cv-robin.duale.fr/fr/perspectives/{slug_fr}.html")
    print("\nProchaines etapes :")
    print("  1. git add + commit + push pour deployer le draft")
    print("  2. Retravaille l'article depuis l'admin (/admin/index.html)")
    print("  3. python publish_article.py article_input.json pour la mise en ligne complete")


if __name__ == "__main__":
    main()
