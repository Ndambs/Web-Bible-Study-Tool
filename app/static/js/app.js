// Small, dependency-free progressive enhancement. The app works fully
// without JS for reading; this file adds the mark-as-read button,
// left/right arrow-key day navigation, the "open the original source"
// confirmation modal, and the dark/light theme toggle.

(function () {
  "use strict";

  function markRead() {
    var btn = document.getElementById("mark-read-btn");
    if (!btn) return;

    btn.addEventListener("click", function () {
      var testament = btn.dataset.testament;
      var day = btn.dataset.day;
      var currentlyDone = btn.getAttribute("aria-pressed") === "true";
      var nextDone = !currentlyDone;

      fetch("/progress/mark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ testament: testament, day_number: day, done: nextDone }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (!data.ok) return;
          btn.setAttribute("aria-pressed", String(nextDone));
          btn.classList.toggle("btn-done", nextDone);
          var label = btn.querySelector(".mark-read-label");
          if (label) {
            label.textContent = nextDone ? "Marked as read" : "Mark this day as read";
          }
        })
        .catch(function () { /* offline or server hiccup: silently ignore */ });
    });
  }

  function keyboardPaging() {
    var article = document.querySelector(".sermonette");
    if (!article) return;

    document.addEventListener("keydown", function (e) {
      if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
      var modal = document.getElementById("source-modal");
      if (modal && !modal.hasAttribute("hidden")) return;

      var prev = document.querySelector(".pager-prev");
      var next = document.querySelector(".pager-next");
      if (e.key === "ArrowLeft" && prev) window.location.href = prev.href;
      if (e.key === "ArrowRight" && next) window.location.href = next.href;
    });
  }

  // ------------------------------------------------------------------
  // "Read the original" confirmation modal for the Voice from Church
  // History block. Only wired up on blocks carrying data-source-url
  // (set server-side only when a real, stable free source is known to
  // exist for that expositor).
  // ------------------------------------------------------------------
  function sourceModal() {
    var trigger = document.getElementById("voice-block");
    var modal = document.getElementById("source-modal");
    if (!trigger || !modal) return;

    var titleEl = document.getElementById("source-modal-title");
    var bodyEl = document.getElementById("source-modal-body");
    var confirmBtn = document.getElementById("source-modal-confirm");
    var cancelBtn = document.getElementById("source-modal-cancel");
    var lastFocused = null;

    function open() {
      var name = trigger.dataset.sourceName;
      var label = trigger.dataset.sourceLabel;
      titleEl.textContent = "Read " + name + "'s original teaching?";
      bodyEl.textContent = (label || ("Visit " + name + "'s original writing or sermons.")) +
        " This will open in a new browser tab.";
      lastFocused = document.activeElement;
      modal.removeAttribute("hidden");
      confirmBtn.focus();
      document.addEventListener("keydown", onKeydown);
    }

    function close() {
      modal.setAttribute("hidden", "");
      document.removeEventListener("keydown", onKeydown);
      if (lastFocused) lastFocused.focus();
    }

    function onKeydown(e) {
      if (e.key === "Escape") close();
    }

    trigger.addEventListener("click", open);
    trigger.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open();
      }
    });

    confirmBtn.addEventListener("click", function () {
      var url = trigger.dataset.sourceUrl;
      close();
      if (url) window.open(url, "_blank", "noopener");
    });
    cancelBtn.addEventListener("click", close);
    modal.addEventListener("click", function (e) {
      if (e.target === modal) close();
    });
  }

  // ------------------------------------------------------------------
  // Dark / light theme toggle. Initial theme is set synchronously in
  // base.html's <head> (before paint); this only handles the switch
  // and persistence from here on.
  // ------------------------------------------------------------------
  function themeToggle() {
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;

    function reflect(theme) {
      var isDark = theme === "dark";
      btn.setAttribute("aria-pressed", String(isDark));
      var label = btn.querySelector(".theme-toggle-label");
      if (label) label.textContent = isDark ? "Light mode" : "Dark mode";
    }

    reflect(document.documentElement.getAttribute("data-theme") || "light");

    btn.addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme") || "light";
      var next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("bsg-theme", next); } catch (e) { /* ignore */ }
      reflect(next);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    markRead();
    keyboardPaging();
    sourceModal();
    themeToggle();
  });
})();
