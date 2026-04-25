(function () {
  var el = document.getElementById('persp-nav');
  if (!el) return;

  var path = window.location.pathname;
  var langMatch = path.match(/^\/(fr|en)\//);
  if (!langMatch) return;
  var lang = langMatch[1];

  var slugMatch = path.match(/\/perspectives\/([^/]+)\.html$/);
  if (!slugMatch) return;
  var currentSlug = slugMatch[1];

  var labels = {
    fr: { next: 'Article suivant', prev: 'Article précédent', related: 'À lire aussi', read: "Lire l'article" },
    en: { next: 'Next article', prev: 'Previous article', related: 'Related articles', read: 'Read article' }
  };
  var lbl = labels[lang];

  fetch('/assets/perspectives.json')
    .then(function (r) { return r.json(); })
    .then(function (articles) {
      var slugKey = 'slug_' + lang;
      var titleKey = 'title_' + lang;
      var tagsKey = 'tags_' + lang;

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
    })
    .catch(function () {});
}());
