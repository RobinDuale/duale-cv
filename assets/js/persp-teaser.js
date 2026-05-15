(function () {
  var el = document.getElementById('persp-teaser');
  if (!el) return;

  var path = window.location.pathname;
  var langMatch = path.match(/^\/(fr|en)\//);
  if (!langMatch) return;
  var lang = langMatch[1];

  var labels = {
    fr: {
      title: 'Mes derniers articles',
      subtitle: "sur la création de valeur, la finance, l'IA, les fonds d'investissement et le leadership.",
      all: 'Tous les articles →',
      link: '/fr/perspectives/'
    },
    en: {
      title: 'Latest articles',
      subtitle: 'on value creation, finance, AI, investment funds and leadership.',
      all: 'All articles →',
      link: '/en/perspectives/'
    }
  };
  var lbl = labels[lang];

  fetch('/assets/perspectives.json')
    .then(function (r) { return r.json(); })
    .then(function (articles) {
      var published = articles.filter(function (a) { return !a.draft; });
      var last3 = published.slice(-3).reverse();

      var slugKey     = 'slug_'     + lang;
      var titleKey    = 'title_'    + lang;
      var subtitleKey = 'subtitle_' + lang;
      var dateKey     = 'date_'     + lang;
      var imageKey    = 'image_'    + lang;
      var altKey      = 'alt_'      + lang;
      var excerptKey  = 'excerpt_'  + lang;

      var cards = '';
      for (var i = 0; i < last3.length; i++) {
        var a = last3[i];
        var sub = a[subtitleKey] || '';
        var titleHtml = a[titleKey] + (sub ? '<br><em>' + sub + '</em>' : '');
        cards += '<a class="persp-teaser-card" href="/' + lang + '/perspectives/' + a[slugKey] + '.html">'
          + '<img src="' + a[imageKey] + '" alt="' + a[altKey] + '" class="persp-card-img" width="800" height="420" loading="lazy"/>'
          + '<div class="persp-teaser-card-body">'
          + '<div class="persp-card-date">' + a[dateKey] + '</div>'
          + '<div class="persp-card-title">' + titleHtml + '</div>'
          + '<p class="persp-card-excerpt">' + a[excerptKey] + '</p>'
          + '</div>'
          + '</a>';
      }

      el.innerHTML = '<section class="persp-teaser" aria-label="Perspectives">'
        + '<div class="persp-teaser-inner">'
        + '<div class="persp-teaser-header">'
        + '<div>'
        + '<h2 class="persp-section-title">' + lbl.title + '</h2>'
        + '<p class="section-subtitle">' + lbl.subtitle + '</p>'
        + '</div>'
        + '<a class="persp-card-link" href="' + lbl.link + '">' + lbl.all + '</a>'
        + '</div>'
        + '<div class="persp-teaser-grid">' + cards + '</div>'
        + '</div>'
        + '</section>';
    })
    .catch(function () {});
}());
