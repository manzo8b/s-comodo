/* S-COMODO: HTML Comment Box.
 * The widget and its stylesheet are fetched only when a reader actively
 * requests comments. No consent is stored locally or across page views.
 * Moderator ID and options are public embed parameters supplied by owner.
 */
(function () {
  "use strict";
  var section = document.querySelector("[data-hcb-comments]");
  if (!section) return;
  var trigger = section.querySelector("#comment-load-button");
  var box = section.querySelector("#HCB_comment_box");
  var status = section.querySelector("#comment-load-status");
  if (!trigger || !box || !status) return;

  trigger.addEventListener("click", function () {
    if (trigger.disabled) return;
    trigger.disabled = true;
    status.textContent = section.getAttribute("data-comment-lang") === "es" ? "Cargando comentarios…" : (section.getAttribute("data-comment-lang") === "en" ? "Loading comments…" : "Caricamento dei commenti…");
    box.hidden = false;
    var pageUrl = section.getAttribute("data-comment-page") || window.location.href.split(/[?#]/)[0];

    var isEnglish = section.getAttribute("data-comment-lang") === "en";
    var isSpanish = section.getAttribute("data-comment-lang") === "es";
    var ui = isSpanish ? {"comments_header":"Comentarios","name_label":"Nombre","content_label":"Escribe tu comentario","submit":"Publicar","no_comments_msg":"Todavía no hay comentarios. ¡Inicia la conversación!","add":"Añadir comentario","again":"Escribir otro comentario","anonymous":"Anónimo","reply":"Responder","flag":"Denunciar","like":"Me gusta","said":"dijo:","showing":"Mostrando","to":"a","days_ago":"días atrás","hours_ago":"horas atrás","minutes_ago":"minutos atrás","within_the_last_minute":"hace menos de un minuto","msg_thankyou":"¡Gracias por tu comentario!","msg_approval":"Tu comentario está pendiente de revisión.","msg_approval_required":"El comentario aparecerá después de los controles del servicio.","err_bad_html":"El comentario contiene HTML no permitido.","err_bad_email":"Correo electrónico no válido.","err_too_frequent":"Espera unos segundos antes de comentar.","err_comment_empty":"Escribe un mensaje antes de publicarlo.","err_denied":"No se ha aceptado el comentario.","err_unknown":"El comentario fue bloqueado. Inténtalo más tarde.","err_spam":"Mensaje detectado como spam.","err_blocked":"El servicio ha bloqueado este mensaje."} : isEnglish ? {
      comments_header: "Comments",
      name_label: "Name",
      content_label: "Write your comment",
      submit: "Post",
      no_comments_msg: "No comments yet. Start the conversation!",
      add: "Add a comment",
      again: "Write another comment",
      anonymous: "Anonymous",
      reply: "Reply",
      flag: "Report",
      like: "Like",
      said: "said:",
      showing: "Showing",
      to: "to",
      days_ago: "days ago",
      hours_ago: "hours ago",
      minutes_ago: "minutes ago",
      within_the_last_minute: "less than a minute ago",
      msg_thankyou: "Thanks for your comment!",
      msg_approval: "Your comment is awaiting review.",
      msg_approval_required: "Your comment will appear after the provider's checks.",
      err_bad_html: "Your comment contains unsupported HTML.",
      err_bad_email: "Invalid email address.",
      err_too_frequent: "Please wait before commenting again.",
      err_comment_empty: "Please write a comment.",
      err_denied: "The comment was not accepted.",
      err_unknown: "Comment blocked. Please try later.",
      err_spam: "This message was detected as spam.",
      err_blocked: "The provider blocked this message."
    } : {
      PAGE: pageUrl,
      comments_header: "Commenti",
      name_label: "Nome",
      content_label: "Scrivi il tuo commento",
      submit: "Pubblica",
      no_comments_msg: "Non ci sono ancora commenti. Inizia la discussione!",
      add: "Aggiungi un commento",
      again: "Scrivi un altro commento",
      anonymous: "Anonimo",
      reply: "Rispondi",
      flag: "Segnala",
      like: "Mi piace",
      said: "ha scritto:",
      showing: "Mostrati",
      to: "a",
      days_ago: "giorni fa",
      hours_ago: "ore fa",
      minutes_ago: "minuti fa",
      within_the_last_minute: "meno di un minuto fa",
      msg_thankyou: "Grazie per il tuo commento!",
      msg_approval: "Il commento è in attesa di verifica.",
      msg_approval_required: "Il commento comparirà dopo i controlli del servizio.",
      err_bad_html: "Il commento contiene codice HTML non consentito.",
      err_bad_email: "Indirizzo email non valido.",
      err_too_frequent: "Attendi qualche secondo prima di commentare nuovamente.",
      err_comment_empty: "Scrivi un messaggio prima di pubblicarlo.",
      err_denied: "Il commento non è stato accettato.",
      err_unknown: "Il commento è stato bloccato. Riprova più tardi.",
      err_spam: "Il messaggio è stato rilevato come spam.",
      err_blocked: "Il messaggio è stato bloccato dai filtri del servizio."
    };
    window.hcb_user = Object.assign({}, window.hcb_user || {}, ui, {PAGE: pageUrl});

    var stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = "https://www.htmlcommentbox.com/static/skins/bootstrap/twitter-bootstrap.css?v=0";
    document.head.appendChild(stylesheet);

    var script = document.createElement("script");
    script.type = "text/javascript";
    script.id = "hcb";
    script.async = true;
    script.src = "https://www.htmlcommentbox.com/jread?page=" +
      encodeURIComponent(pageUrl).replace(/\+/g, "%2B") +
      "&mod=%241%24wq1rdBcg%241Au32fLvprMu3bQ6UNOpC1" +
      "&opts=16670&num=10&ts=1792938226098";
    script.onload = function () {
      status.textContent = "";
      var prompt = section.querySelector("#comment-privacy-prompt");
      if (prompt) prompt.hidden = true;
    };
    script.onerror = function () {
      status.textContent = isSpanish ? "Los comentarios no están disponibles ahora. Inténtalo más tarde." : (isEnglish ? "Comments are unavailable right now. Please try again." : "I commenti non sono disponibili al momento. Controlla la connessione o riprova.");
      trigger.disabled = false;
      box.hidden = true;
    };
    document.head.appendChild(script);
  });
})();
