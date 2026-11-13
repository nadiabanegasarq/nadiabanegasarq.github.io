/* ==========================================================================
   Nadia Banegas | Arquitecta — Interacciones
   ========================================================================== */
(function () {
  'use strict';

  var wa = (window.SITE_CONTENT || {}).whatsapp || {
    number: '5493547662066',
    defaultMessage: 'Hola Nadia, estuve viendo tu página web y quisiera hacerte una consulta sobre un proyecto.',
    serviceMessage: 'Hola Nadia, estuve viendo tu página web y quisiera hacerte una consulta sobre el servicio de {servicio}.'
  };
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- WhatsApp con mensaje precargado ---------- */
  document.querySelectorAll('[data-wa]').forEach(function (el) {
    var service = el.getAttribute('data-service');
    var message = el.getAttribute('data-msg') ||
      (service ? wa.serviceMessage.replace('{servicio}', service.toLowerCase()) : wa.defaultMessage);
    el.setAttribute('href', 'https://wa.me/' + wa.number + '?text=' + encodeURIComponent(message));
  });

  /* ---------- Encabezado ---------- */
  var header = document.querySelector('[data-header]');
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menú móvil ---------- */
  var toggle = document.querySelector('[data-nav-toggle]');
  var panel = document.querySelector('[data-nav-panel]');
  var mqDesktop = window.matchMedia('(min-width: 960px)');
  function setMenu(open) {
    document.body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = open ? 'Cerrar menú' : 'Abrir menú';
    if (!mqDesktop.matches) { if (open) panel.removeAttribute('inert'); else panel.setAttribute('inert', ''); }
  }
  function syncPanel() {
    if (mqDesktop.matches) { panel.removeAttribute('inert'); setMenu(false); }
    else if (!document.body.classList.contains('nav-open')) panel.setAttribute('inert', '');
  }
  toggle.addEventListener('click', function () { setMenu(!document.body.classList.contains('nav-open')); });
  panel.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.body.classList.contains('nav-open')) { setMenu(false); toggle.focus(); }
  });
  (mqDesktop.addEventListener ? mqDesktop.addEventListener('change', syncPanel) : mqDesktop.addListener(syncPanel));
  syncPanel();

  /* ---------- Acordeón ---------- */
  document.querySelectorAll('[data-accordion] .acc-trigger').forEach(function (btn) {
    var panelEl = document.getElementById(btn.getAttribute('aria-controls'));
    btn.addEventListener('click', function () {
      var expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
      if (reduceMotion) { panelEl.hidden = expanded; return; }
      if (expanded) {
        panelEl.style.height = panelEl.scrollHeight + 'px';
        requestAnimationFrame(function () { panelEl.style.height = '0px'; });
        panelEl.addEventListener('transitionend', function done() {
          panelEl.hidden = true; panelEl.style.height = '';
          panelEl.removeEventListener('transitionend', done);
        });
      } else {
        panelEl.hidden = false;
        var h = panelEl.scrollHeight;
        panelEl.style.height = '0px';
        requestAnimationFrame(function () { panelEl.style.height = h + 'px'; });
        panelEl.addEventListener('transitionend', function done() {
          panelEl.style.height = '';
          panelEl.removeEventListener('transitionend', done);
        });
      }
    });
  });

  /* ---------- Categoría activa (preguntas frecuentes) ---------- */
  var faqNav = document.querySelectorAll('.faq-nav ul a');
  if (faqNav.length && 'IntersectionObserver' in window) {
    var faqObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        faqNav.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id); });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.faq-group').forEach(function (g) { faqObs.observe(g); });
  }

  /* ---------- Visor de fotos ---------- */
  var box = document.querySelector('[data-lightbox]');
  if (box) {
    var img = box.querySelector('[data-lb-img]');
    var cap = box.querySelector('[data-lb-caption]');
    var items = [], index = 0, lastFocus = null, touchX = null;

    function show(i) {
      index = (i + items.length) % items.length;
      var it = items[index];
      img.src = it.getAttribute('href');
      img.alt = it.getAttribute('data-caption') || '';
      cap.textContent = (it.getAttribute('data-caption') || '') + '  ·  ' + (index + 1) + ' / ' + items.length;
      var next = items[(index + 1) % items.length];
      if (next) { var pre = new Image(); pre.src = next.getAttribute('href'); }
    }
    function open(gallery, i) {
      items = Array.prototype.slice.call(document.querySelectorAll('[data-gallery="' + gallery + '"]'));
      if (!items.length) return;
      lastFocus = document.activeElement;
      box.hidden = false;
      document.body.classList.add('lightbox-open');
      show(i || 0);
      box.querySelector('[data-lb-close]').focus();
    }
    function close() {
      box.hidden = true;
      document.body.classList.remove('lightbox-open');
      img.removeAttribute('src');
      if (lastFocus) lastFocus.focus();
    }
    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('[data-open-gallery]');
      if (trigger) open(trigger.getAttribute('data-open-gallery'), +trigger.getAttribute('data-index') || 0);
    });
    box.querySelector('[data-lb-close]').addEventListener('click', close);
    box.querySelector('[data-lb-prev]').addEventListener('click', function () { show(index - 1); });
    box.querySelector('[data-lb-next]').addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') show(index + 1);
      else if (e.key === 'ArrowLeft') show(index - 1);
      else if (e.key === 'Tab') {
        var f = box.querySelectorAll('button');
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    box.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
      touchX = null;
    }, { passive: true });
  }
})();
