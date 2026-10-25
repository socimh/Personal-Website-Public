// EN | 中文 language toggle for the bilingual site.
// The English site lives at the root, the Chinese site under /zh/, with one
// counterpart page per English page. Both navbars carry a right-hand item
// labelled "EN | 中文"; this script splits it into two links, marks the
// current language, and points the other label at the matching page.
// Also adds hreflang alternates to <head> for search engines.
(function () {
  "use strict";

  // Pages that exist in both languages (file names, "" = site root).
  var PAGES = ["", "index.html", "research.html", "books.html",
               "teaching.html", "slides.html", "software.html"];

  var path = window.location.pathname;
  var m = path.match(/^(.*?\/)(zh\/)?([^\/]*)$/);
  if (!m) return;
  var root = m[1], isZh = !!m[2], file = m[3];
  var shared = PAGES.indexOf(file) !== -1;

  var enHref = root + (shared ? file : "");
  var zhHref = root + "zh/" + (shared ? file : "");

  // Quarto drops aria-label on text navbar items, so find the item by its label.
  var link = Array.prototype.filter.call(
    document.querySelectorAll(".navbar a.nav-link"),
    function (a) { return a.textContent.replace(/\s+/g, "") === "EN|中文"; }
  )[0];
  if (link) {
    var item = link.parentNode;
    var wrap = document.createElement("span");
    wrap.className = "nav-link lang-toggle";
    wrap.innerHTML =
      '<a href="' + enHref + '" lang="en"' + (isZh ? "" : ' class="active" aria-current="true"') + ">EN</a>" +
      '<span class="lang-sep" aria-hidden="true">|</span>' +
      '<a href="' + zhHref + '" lang="zh"' + (isZh ? ' class="active" aria-current="true"' : "") + ">中文</a>";
    item.replaceChild(wrap, link);
  }

  if (shared) {
    [["en", enHref], ["zh", zhHref]].forEach(function (p) {
      var l = document.createElement("link");
      l.rel = "alternate";
      l.hreflang = p[0];
      l.href = window.location.origin + p[1];
      document.head.appendChild(l);
    });
  }
})();
