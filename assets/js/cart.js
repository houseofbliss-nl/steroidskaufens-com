/**
 * Cart.js — Client-side cart for steroidskaufen.com static clone
 * Uses localStorage, intercepts add-to-cart before PrestaShop AJAX handler.
 */
(function () {
  'use strict';

  var CART_KEY = 'sc_cart';

  function getCart() {
    try {
      return JSON.parse(localStorage.getItem(CART_KEY)) || {};
    } catch (_) {
      return {};
    }
  }

  function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
  }

  // ── Public API ───────────────────────────────────────────

  window.SteroidCart = {
    getCart: getCart,

    add: function (id, name, price, image, qty, url) {
      if (!id) return;
      qty = parseInt(qty, 10) || 1;
      var cart = getCart();
      if (cart[id]) {
        cart[id].qty += qty;
        if (cart[id].qty < 1) cart[id].qty = 1;
        if (url) cart[id].url = url;
      } else {
        cart[id] = { id: id, name: name, price: price, image: image, qty: qty, url: url || '' };
      }
      saveCart(cart);
      this.updateUI();
    },

    remove: function (id) {
      var cart = getCart();
      delete cart[id];
      saveCart(cart);
      this.updateUI();
    },

    updateQty: function (id, qty) {
      qty = parseInt(qty, 10) || 0;
      if (qty <= 0) { this.remove(id); return; }
      var cart = getCart();
      if (cart[id]) {
        cart[id].qty = qty;
        saveCart(cart);
        this.updateUI();
      }
    },

    clear: function () {
      localStorage.removeItem(CART_KEY);
      this.updateUI();
    },

    getCount: function () {
      var cart = getCart();
      var n = 0;
      for (var k in cart) if (cart.hasOwnProperty(k)) n += cart[k].qty;
      return n;
    },

    getTotal: function () {
      var cart = getCart();
      var t = 0;
      for (var k in cart) if (cart.hasOwnProperty(k)) t += cart[k].price * cart[k].qty;
      return t;
    },

    // ── UI updates ──────────────────────────────────────────

    updateUI: function () {
      var count = this.getCount();
      document.querySelectorAll('.cart-products-count').forEach(function (el) {
        el.textContent = count;
      });
      document.querySelectorAll('.blockcart').forEach(function (el) {
        if (count > 0) {
          el.classList.remove('inactive');
          el.classList.add('active');
        } else {
          el.classList.add('inactive');
          el.classList.remove('active');
        }
      });
    },

    // ── Initialise ──────────────────────────────────────────

    init: function () {
      this.enableDisabledButtons();
      this.interceptAddToCartClicks();
      this.interceptAddToCartSubmit();
      this.makeCartHeaderClickable();
      this.updateUI();
    },

    // ── Shared price parser ──────────────────────────────────

    _parsePrice: function (text) {
      if (!text) return 0;
      var v = String(text).trim();
      if (/^\d+(\.\d+)?$/.test(v)) return parseFloat(v) || 0;
      v = v.replace(/[^\d,\-]/g, '').replace(/\./g, '').replace(',', '.');
      return parseFloat(v) || 0;
    },

    /** Extract product details from the DOM and add to cart */
    _extractAndAdd: function (form, id, qty) {
      var name = '';
      var price = 0;
      var image = '';
      var url = '';

      if (form.id === 'add-to-cart-or-refresh') {
        // Product detail page
        var h1 = document.querySelector('h1[itemprop="name"]');
        if (h1) name = h1.textContent.trim();

        var priceSpan = document.querySelector('span[itemprop="price"]');
        if (priceSpan) {
          price = this._parsePrice(priceSpan.getAttribute('content') || priceSpan.textContent);
        }

        var coverImg = document.querySelector('.product-cover img') || document.querySelector('.js-qv-product-cover');
        if (coverImg) image = coverImg.src;

        // Product URL from current page
        url = window.location.pathname;
      } else {
        // Category listing page — walk up to product container
        var container =
          form.closest('.thumbnail-container') ||
          form.closest('.product-miniature') ||
          form.closest('article') ||
          form.parentElement;

        if (container) {
          var nameEl =
            container.querySelector('.product-title a') ||
            container.querySelector('.product-title') ||
            container.querySelector('[itemprop="name"]');
          if (nameEl) {
            name = nameEl.textContent.trim();
            // Grab URL from the same anchor
            if (nameEl.tagName === 'A') url = nameEl.getAttribute('href');
          }

          var priceEl =
            container.querySelector('[itemprop="price"]') ||
            container.querySelector('.price') ||
            container.querySelector('.current-price span');
          if (priceEl) {
            price = this._parsePrice(priceEl.getAttribute('content') || priceEl.textContent);
          }

          var imgEl =
            container.querySelector('img[src*="home_default"]') ||
            container.querySelector('img[src*="large_default"]') ||
            container.querySelector('img');
          if (imgEl) image = imgEl.src;
        }
      }

      this.add(id, name, price, image, qty, url);
    },

    /** Remove disabled from add-to-cart buttons on product pages */
    enableDisabledButtons: function () {
      document.querySelectorAll('[data-button-action="add-to-cart"][disabled]').forEach(function (btn) {
        btn.removeAttribute('disabled');
      });
    },

    /** Intercept add-to-cart clicks BEFORE PrestaShop jQuery handler */
    interceptAddToCartClicks: function () {
      var self = this;
      document.addEventListener(
        'click',
        function (e) {
          var btn = e.target.closest('[data-button-action="add-to-cart"]');
          if (!btn) return;

          e.preventDefault();
          e.stopPropagation();

          var form = btn.closest('form');
          if (!form) return;

          var id = form.querySelector('[name="id_product"]');
          var qtyEl = form.querySelector('[name="qty"]');
          var idVal = id ? id.value : '';
          var qtyVal = qtyEl ? parseInt(qtyEl.value, 10) || 1 : 1;
          if (!idVal) return;

          self._extractAndAdd(form, idVal, qtyVal);
        },
        true
      );
    },

    /** Safety net: intercept form submit events (Enter key in inputs) */
    interceptAddToCartSubmit: function () {
      var self = this;
      document.addEventListener(
        'submit',
        function (e) {
          var form = e.target;
          if (
            form.id === 'add-to-cart-or-refresh' ||
            form.classList.contains('cart-form-url') ||
            form.querySelector('[data-button-action="add-to-cart"]')
          ) {
            e.preventDefault();
            e.stopPropagation();

            var id = form.querySelector('[name="id_product"]');
            var qtyEl = form.querySelector('[name="qty"]');
            var idVal = id ? id.value : '';
            var qtyVal = qtyEl ? parseInt(qtyEl.value, 10) || 1 : 1;
            if (!idVal) return;

            self._extractAndAdd(form, idVal, qtyVal);
          }
        },
        true
      );
    },

    makeCartHeaderClickable: function () {
      document.querySelectorAll('#_desktop_cart .blockcart, #_mobile_cart .blockcart').forEach(function (el) {
        el.style.cursor = 'pointer';
        el.addEventListener('click', function () {
          window.location.href = '/de/warenkorb.html';
        });
      });
    },
  };

  // ── Auto-boot ────────────────────────────────────────────

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      window.SteroidCart.init();
    });
  } else {
    window.SteroidCart.init();
  }
})();
