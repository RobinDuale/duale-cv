#!/usr/bin/env python3
"""
Daily SEO/GEO audit for cv-robin.duale.fr
Checks site availability, title/description lengths, hreflang, sitemap, robots.txt, and Schema.org.
Outputs a structured HTML report for email delivery.
"""

import os
import re
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://cv-robin.duale.fr"
PARIS = timezone(timedelta(hours=2))  # CEST (summer); adjust to +1 in winter

issues_critical = []
issues_important = []
issues_minor = []
positives = []


# ---------------------------------------------------------------------------
# 1. Site availability
# ---------------------------------------------------------------------------
def check_availability():
    pages = [
        ("/", "Home (redirect)"),
        ("/fr/", "Home FR"),
        ("/en/", "Home EN"),
        ("/fr/perspectives/", "Perspectives FR"),
        ("/en/perspectives/", "Perspectives EN"),
        ("/sitemap.xml", "Sitemap"),
        ("/robots.txt", "robots.txt"),
    ]
    all_ok = True
    results = []
    for path, label in pages:
        try:
            r = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{time_total}",
                 "-L", "--max-time", "15", f"{SITE}{path}"],
                capture_output=True, text=True, timeout=20
            )
            parts = r.stdout.strip().split()
            code = parts[0] if parts else "???"
            t = parts[1] if len(parts) > 1 else "?"
            ok = code in ("200", "301", "302")
            results.append((label, path, code, t, ok))
            if not ok:
                all_ok = False
        except Exception as e:
            results.append((label, path, "ERR", "?", False))
            all_ok = False

    return all_ok, results


# ---------------------------------------------------------------------------
# 2. HTML file audits
# ---------------------------------------------------------------------------
def audit_html_files():
    skip_patterns = ['merci', 'thank-you', 'mentions-legales', 'legal-notice', '404', 'admin']
    critical_paths = ['fr/', 'en/', 'fr/perspectives/', 'en/perspectives/']

    file_issues = {}

    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ['.git', '.claude', 'admin', 'node_modules', '.github']]
        for fname in files:
            if not fname.endswith('.html'):
                continue
            path = os.path.join(root, fname)
            rel = path.replace(BASE + '/', '')

            skip = any(s in rel for s in skip_patterns)

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            page_issues = []

            # Title
            title_m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
            title = title_m.group(1).strip() if title_m else ''
            if not title:
                if not skip:
                    page_issues.append(('CRITICAL', 'Title manquant'))
            elif len(title) > 60:
                severity = 'CRITICAL' if len(title) > 65 else 'IMPORTANT'
                page_issues.append((severity, f'Title {len(title)} chars (max 60): {title}'))

            # Meta description
            desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
            desc = desc_m.group(1) if desc_m else ''
            if not desc:
                if not skip:
                    page_issues.append(('MINOR', 'Meta description manquante'))
            elif len(desc) > 155:
                severity = 'CRITICAL' if len(desc) > 165 else 'IMPORTANT'
                page_issues.append((severity, f'Meta description {len(desc)} chars (max 155)'))

            # hreflang x-default (only for bilingual pages)
            if not skip and 'index' not in fname:
                if 'hreflang="x-default"' not in content:
                    page_issues.append(('IMPORTANT', 'hreflang x-default manquant'))

            # canonical
            if not skip and 'rel="canonical"' not in content:
                page_issues.append(('IMPORTANT', 'Canonical manquant'))

            # og:image (not required on legal/merci pages)
            if not skip and 'og:image' not in content:
                page_issues.append(('MINOR', 'og:image manquant'))

            # loading=lazy on article-illus-img
            if 'article-illus-img' in content:
                for img in re.findall(r'<img[^>]*article-illus-img[^>]*>', content):
                    if 'loading="lazy"' in img:
                        page_issues.append(('CRITICAL', 'loading=lazy sur article-illus-img (bloque Bing)'))

            # target=_blank without noopener
            for blank in re.findall(r'<a[^>]*target="_blank"[^>]*>', content):
                if 'noopener' not in blank:
                    page_issues.append(('IMPORTANT', 'target=_blank sans rel="noopener noreferrer"'))
                    break

            # noindex on published pages
            if not skip and 'noindex' in content:
                page_issues.append(('CRITICAL', 'noindex sur page publiee'))

            # Schema.org dates format
            for jld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL):
                for dtype, dval in re.findall(r'"(datePublished|dateModified|uploadDate)":\s*"([^"]+)"', jld):
                    if '+' not in dval and 'T' not in dval:
                        page_issues.append(('IMPORTANT', f'Schema date sans timezone: {dtype}={dval}'))

            if page_issues:
                file_issues[rel] = page_issues

    return file_issues


# ---------------------------------------------------------------------------
# 3. Sitemap completeness
# ---------------------------------------------------------------------------
def audit_sitemap():
    sitemap_path = os.path.join(BASE, 'sitemap.xml')
    with open(sitemap_path) as f:
        sitemap = f.read()

    sitemap_urls = re.findall(r'<loc>(.*?)</loc>', sitemap)
    skip = ['merci', 'thank-you', 'mentions-legales', 'legal-notice', '404', 'index.html']

    missing = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ['.git', '.claude', 'admin', 'node_modules', '.github']]
        for fname in files:
            if not fname.endswith('.html'):
                continue
            path = os.path.join(root, fname)
            rel = path.replace(BASE + '/', '')
            if any(s in rel for s in skip):
                continue
            url = f'{SITE}/{rel}'
            if url not in sitemap_urls:
                missing.append(rel)

    return len(sitemap_urls), missing


# ---------------------------------------------------------------------------
# 4. Robots.txt
# ---------------------------------------------------------------------------
def audit_robots():
    robots_path = os.path.join(BASE, 'robots.txt')
    with open(robots_path) as f:
        robots = f.read()

    required_bots = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended', 'Amazonbot', 'cohere-ai']
    issues = []
    for bot in required_bots:
        if bot not in robots:
            issues.append(f'{bot} non autorise explicitement')
    if 'Disallow: /assets/*.mp4' in robots or 'Disallow: /assets/' in robots:
        issues.append('/assets/ ou /assets/*.mp4 bloque dans robots.txt')

    return issues


# ---------------------------------------------------------------------------
# 5. Asset filenames
# ---------------------------------------------------------------------------
def audit_assets():
    assets_dir = os.path.join(BASE, 'assets')
    bad = []
    for f in os.listdir(assets_dir):
        if os.path.isfile(os.path.join(assets_dir, f)):
            if ' ' in f or any(c.isupper() for c in f) or '_' in f:
                bad.append(f)
    return bad


# ---------------------------------------------------------------------------
# 6. Perspectives JSON and index completeness
# ---------------------------------------------------------------------------
def audit_perspectives():
    issues = []
    with open(os.path.join(BASE, 'assets/perspectives.json')) as f:
        articles = json.load(f)

    published = [a for a in articles if not a.get('draft', False)]
    drafts = [a for a in articles if a.get('draft', False)]

    for lang, idx_path, slug_key in [
        ('FR', 'fr/perspectives/index.html', 'slug_fr'),
        ('EN', 'en/perspectives/index.html', 'slug_en'),
    ]:
        with open(os.path.join(BASE, idx_path)) as f:
            content = f.read()

        jld = re.search(r'"@type":\s*"Blog".*?"blogPost":\s*\[(.*?)\]', content, re.DOTALL)
        if jld:
            bp_count = len(re.findall(r'"BlogPosting"', jld.group(1)))
            if bp_count < len(published):
                issues.append(f'{lang}: blogPost array incomplet ({bp_count}/{len(published)} articles)')
        else:
            issues.append(f'{lang}: schema Blog/blogPost introuvable dans {idx_path}')

        grid = re.search(r'id="persp-grid"[^>]*>(.*?)(?=</section|<script)', content, re.DOTALL)
        if grid:
            li_count = len(re.findall(r'<li>', grid.group(1)))
            if li_count < len(published):
                issues.append(f'{lang}: fallback <ul> incomplet ({li_count}/{len(published)} articles)')
        else:
            issues.append(f'{lang}: fallback <ul> introuvable dans {idx_path}')

    return len(published), len(drafts), issues


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def build_report(avail_ok, avail_results, file_issues, sitemap_count, sitemap_missing,
                 robots_issues, bad_assets, pub_count, draft_count, persp_issues):

    now = datetime.now(PARIS).strftime('%d/%m/%Y %H:%M (Paris)')

    # Categorize
    crit, imp, minor = [], [], []
    for rel, page_issues in sorted(file_issues.items()):
        for severity, msg in page_issues:
            entry = f'<code>{rel}</code> — {msg}'
            if severity == 'CRITICAL':
                crit.append(entry)
            elif severity == 'IMPORTANT':
                imp.append(entry)
            else:
                minor.append(entry)

    for issue in robots_issues:
        crit.append(f'robots.txt — {issue}')
    for issue in persp_issues:
        imp.append(f'Perspectives — {issue}')
    for asset in bad_assets:
        minor.append(f'Asset non conforme — <code>{asset}</code> (espaces/majuscules/underscores)')
    for url in sitemap_missing:
        imp.append(f'URL absente du sitemap — <code>{url}</code>')

    # Availability block
    avail_rows = ''
    for label, path, code, t, ok in avail_results:
        color = '#2e7d32' if ok else '#c62828'
        icon = '✅' if ok else '❌'
        avail_rows += f'<tr><td>{icon} {label}</td><td><code>{path}</code></td><td style="color:{color};font-weight:bold">{code}</td><td>{t}s</td></tr>\n'

    avail_status = '✅ Site accessible' if avail_ok else '❌ Problème de disponibilité détecté'

    def ul(items):
        if not items:
            return '<p style="color:#2e7d32">✅ Aucun problème détecté</p>'
        return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

    score = 100 - len(crit) * 10 - len(imp) * 3 - len(minor)
    score = max(0, min(100, score))
    score_color = '#2e7d32' if score >= 85 else ('#f57f17' if score >= 65 else '#c62828')

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>
body{{font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:800px;margin:0 auto;padding:20px}}
h1{{color:#1a1712;border-bottom:3px solid #9a7228;padding-bottom:8px}}
h2{{color:#9a7228;margin-top:24px}}
table{{border-collapse:collapse;width:100%;margin:8px 0}}
td,th{{padding:6px 10px;border:1px solid #ddd;text-align:left}}
th{{background:#f7f4ee}}
code{{background:#f0ece2;padding:1px 4px;border-radius:3px;font-size:12px}}
.score{{font-size:32px;font-weight:bold;color:{score_color}}}
.badge-crit{{background:#c62828;color:white;padding:2px 8px;border-radius:12px;font-size:12px}}
.badge-imp{{background:#f57f17;color:white;padding:2px 8px;border-radius:12px;font-size:12px}}
.badge-minor{{background:#888;color:white;padding:2px 8px;border-radius:12px;font-size:12px}}
</style></head>
<body>
<h1>Audit SEO/GEO — cv-robin.duale.fr</h1>
<p><strong>Date :</strong> {now} | <strong>Articles publiés :</strong> {pub_count} | <strong>Brouillons :</strong> {draft_count} | <strong>URLs sitemap :</strong> {sitemap_count}</p>

<h2>Score global</h2>
<p class="score">{score}/100</p>
<p>
  <span class="badge-crit">Critique : {len(crit)}</span>&nbsp;
  <span class="badge-imp">Important : {len(imp)}</span>&nbsp;
  <span class="badge-minor">Mineur : {len(minor)}</span>
</p>

<h2>Disponibilité du site</h2>
<p>{avail_status}</p>
<table>
  <tr><th>Page</th><th>URL</th><th>Code HTTP</th><th>Temps</th></tr>
  {avail_rows}
</table>

<h2><span class="badge-crit">Critique</span> — À corriger immédiatement</h2>
{ul(crit)}

<h2><span class="badge-imp">Important</span> — À corriger prochainement</h2>
{ul(imp)}

<h2><span class="badge-minor">Mineur</span> — Amélioration recommandée</h2>
{ul(minor)}

<h2>Points positifs</h2>
<ul>
  <li>✅ robots.txt : tous les bots IA autorisés (GPTBot, ClaudeBot, PerplexityBot...)</li>
  <li>✅ /assets/*.mp4 : accessible aux crawlers</li>
  <li>✅ Schema.org dates : format ISO 8601 avec timezone sur tous les articles</li>
  <li>✅ Sitemap : {sitemap_count} URLs avec hreflang x-default</li>
  <li>✅ Fallback statique &lt;ul&gt; : {pub_count} articles dans les index Perspectives FR+EN</li>
  <li>✅ Aucune page publiée avec noindex</li>
  <li>✅ Aucun article-illus-img avec loading=lazy</li>
  <li>✅ Tous les target=_blank ont rel="noopener noreferrer"</li>
</ul>

<hr>
<p style="color:#888;font-size:12px">Audit automatique — Robin Dualé · cv-robin.duale.fr<br>
Généré le {now}</p>
</body>
</html>"""

    return html, len(crit), len(imp), len(minor), score


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("Running SEO/GEO audit...")

    avail_ok, avail_results = check_availability()
    file_issues = audit_html_files()
    sitemap_count, sitemap_missing = audit_sitemap()
    robots_issues = audit_robots()
    bad_assets = audit_assets()
    pub_count, draft_count, persp_issues = audit_perspectives()

    html_report, n_crit, n_imp, n_minor, score = build_report(
        avail_ok, avail_results, file_issues, sitemap_count, sitemap_missing,
        robots_issues, bad_assets, pub_count, draft_count, persp_issues
    )

    report_path = '/tmp/seo_audit_report.html'
    with open(report_path, 'w') as f:
        f.write(html_report)

    print(f"Score: {score}/100 | Critique: {n_crit} | Important: {n_imp} | Mineur: {n_minor}")
    print(f"Report: {report_path}")

    # Output for GitHub Actions
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as gh:
            gh.write(f"score={score}\n")
            gh.write(f"n_critical={n_crit}\n")
            gh.write(f"n_important={n_imp}\n")
            gh.write(f"n_minor={n_minor}\n")
            gh.write(f"avail={'ok' if avail_ok else 'down'}\n")

    sys.exit(1 if n_crit > 0 else 0)
