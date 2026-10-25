// Subtle scroll-reveal animations for the site.
// Vanilla JS only; disabled when the user prefers reduced motion.
// Elements are hidden by the .reveal-init class (added here, so no-JS
// browsers are unaffected) and shown by .revealed on intersection.
(function () {
  "use strict";

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;

  var targets = document.querySelectorAll(
    ".entry-card, .paper-list li, .quarto-about-solana .about-entity"
  );
  if (!targets.length) return;

  targets.forEach(function (el, i) {
    el.classList.add("reveal-init");
    // Small stagger so grouped items cascade instead of popping together.
    el.style.transitionDelay = Math.min(i % 6, 5) * 50 + "ms";
  });

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -5% 0px" }
  );

  targets.forEach(function (el) {
    io.observe(el);
  });
})();
