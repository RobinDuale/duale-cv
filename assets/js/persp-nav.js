(function () {
  var path = window.location.pathname;
  var langMatch = path.match(/^\/(fr|en)\//);
  if (!langMatch) return;
  var lang = langMatch[1];

  var labels = {
    fr: { next: 'Article suivant', prev: 'Article précédent', related: 'À lire aussi', read: "Lire l'article" },
    en: { next: 'Next article', prev: 'Previous article', related: 'Related articles', read: 'Read article' }
  };
  var lbl = labels[lang];

  fetch('/assets/perspectives.json')
    .then(function (r) { return r.json(); })
    .then(function (articles) {
      if (path.match(/\/perspectives\/$/) || path.match(/\/perspectives\/index\.html$/)) {
        buildGrid(articles, lang);
      } else {
        buildNav(articles, lang, lbl);
      }
    })
    .catch(function () {});

  function buildGrid(articles, lang) {
    var el = document.getElementById('persp-grid');
    if (!el) return;

    var slugKey    = 'slug_'    + lang;
    var titleKey   = 'title_'   + lang;
    var tagsKey    = 'tags_'    + lang;
    var dateKey    = 'date_'    + lang;
    var imageKey   = 'image_'   + lang;
    var altKey     = 'alt_'     + lang;
    var excerptKey = 'excerpt_' + lang;
    var readLabel  = lang === 'fr' ? "Lire l'article" : 'Read article';

    var html = '';
    for (var i = articles.length - 1; i >= 0; i--) {
      var a = articles[i];
      html += '<div class="persp-card">'
        + '<img src="' + a[imageKey] + '" alt="' + a[altKey] + '" class="persp-card-img" width="800" height="420" loading="lazy"/>'
        + '<div class="persp-card-body">'
        + '<div class="persp-card-date">' + a[dateKey] + '</div>'
        + '<div>'
        + '<span class="persp-card-tag">' + a[tagsKey] + '</span>'
        + '<div class="persp-card-title">' + a[titleKey] + '</div>'
        + '<p class="persp-card-excerpt">' + a[excerptKey] + '</p>'
        + '<a class="persp-card-link" href="/' + lang + '/perspectives/' + a[slugKey] + '.html">' + readLabel + '</a>'
        + '</div>'
        + '</div>'
        + '</div>';
    }
    el.innerHTML = html;
  }

  function buildNav(articles, lang, lbl) {
    var el = document.getElementById('persp-nav');
    if (!el) return;

    var slugKey  = 'slug_'  + lang;
    var titleKey = 'title_' + lang;
    var tagsKey  = 'tags_'  + lang;

    var slugMatch = path.match(/\/perspectives\/([^/]+)\.html$/);
    if (!slugMatch) return;
    var currentSlug = slugMatch[1];

    var idx = -1;
    for (var i = 0; i < articles.length; i++) {
      if (articles[i][slugKey] === currentSlug) { idx = i; break; }
    }
    if (idx === -1) return;

    var prev = idx > 0 ? articles[idx - 1] : null;
    var next = idx < articles.length - 1 ? articles[idx + 1] : null;

    var pool = articles.filter(function (_, i) {
      return i !== idx && i !== idx - 1 && i !== idx + 1;
    });
    if (pool.length < 3 && next) pool.push(next);
    if (pool.length < 3 && prev) pool.push(prev);
    var related = pool.slice(0, 3);

    var html = '';

    if (next) {
      html += '<div class="sidebar-section">'
        + '<div class="sidebar-title">' + lbl.next + '</div>'
        + '<p class="sidebar-text" style="margin-bottom:10px">' + next[titleKey] + '</p>'
        + '<a class="persp-card-link" href="/' + lang + '/perspectives/' + next[slugKey] + '.html">' + lbl.read + '</a>'
        + '</div>';
    }

    if (prev) {
      html += '<div class="sidebar-section">'
        + '<div class="sidebar-title">' + lbl.prev + '</div>'
        + '<p class="sidebar-text" style="margin-bottom:10px">' + prev[titleKey] + '</p>'
        + '<a class="persp-card-link" href="/' + lang + '/perspectives/' + prev[slugKey] + '.html">' + lbl.read + '</a>'
        + '</div>';
    }

    if (related.length > 0) {
      html += '<div class="sidebar-section"><div class="sidebar-title">' + lbl.related + '</div>'
        + '<div style="display:flex;flex-direction:column;gap:14px;margin-top:4px">';
      for (var j = 0; j < related.length; j++) {
        var a = related[j];
        html += '<div>'
          + '<div class="persp-card-tag" style="margin-bottom:5px">' + a[tagsKey] + '</div>'
          + '<a class="persp-card-link" href="/' + lang + '/perspectives/' + a[slugKey] + '.html">' + a[titleKey] + '</a>'
          + '</div>';
      }
      html += '</div></div>';
    }

    el.innerHTML = html;
  }
}());
