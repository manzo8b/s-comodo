/* S-COMODO: native share + copy link.
 * Only acts on user interaction. Does not send data to S-COMODO or third parties.
 * No analytics, no social tracking scripts and no artificial reaction counters.
 */
(function () {
  "use strict";
  var actions = document.querySelector("[data-article-actions]");
  if (!actions) return;
  var shareButton = actions.querySelector("[data-share-button]");
  var copyButton = actions.querySelector("[data-copy-button]");
  var status = actions.querySelector("[data-share-status]");
  if (!shareButton || !copyButton || !status) return;

  var lang = actions.getAttribute("data-share-lang") || "it";
  var title = actions.getAttribute("data-share-title") || document.title;
  var url = actions.getAttribute("data-share-url") || window.location.href.split(/[?#]/)[0];
  var messages = {
    it: { copied: "Link copiato. Puoi incollarlo dove preferisci.", failed: "Non è stato possibile copiare il link: selezionalo dalla barra degli indirizzi.", shared: "Condivisione avviata.", error: "La condivisione non è disponibile: prova con Copia link." },
    es: { copied: "Enlace copiado. Puedes pegarlo donde quieras.", failed: "No se ha podido copiar el enlace: cópialo desde la barra de direcciones.", shared: "Se ha iniciado el proceso de compartir.", error: "No se ha podido compartir. Prueba con Copiar enlace." },
    en: { copied: "Link copied. You can paste it wherever you like.", failed: "Unable to copy the link. Copy it from the address bar.", shared: "Sharing opened.", error: "Sharing is unavailable. Try Copy link." }
  };
  var m = messages[lang] || messages.it;
  var clearText = function () { status.textContent = ""; };

  async function copyLink() {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(url);
      } else {
        var field = document.createElement("textarea");
        field.value = url;
        field.setAttribute("readonly", "");
        field.style.position = "fixed";
        field.style.opacity = "0";
        document.body.appendChild(field);
        field.select();
        var successful = document.execCommand("copy");
        document.body.removeChild(field);
        if (!successful) throw new Error("copy unsupported");
      }
      status.textContent = m.copied;
    } catch (e) {
      status.textContent = m.failed;
    }
  }

  shareButton.addEventListener("click", function () {
    clearText();
    if (typeof navigator.share !== "function") {
      copyLink();
      return;
    }
    // The native share must be called synchronously within the user gesture.
    try {
      var sharePromise = navigator.share({ title: title, url: url });
      sharePromise.then(function () {
        status.textContent = m.shared;
      }).catch(function (err) {
        // A deliberate cancellation is not an error.
        if (err && err.name === "AbortError") return;
        status.textContent = m.error;
      });
    } catch (e) {
      status.textContent = m.error;
    }
  });
  copyButton.addEventListener("click", function () { clearText(); copyLink(); });
})();
