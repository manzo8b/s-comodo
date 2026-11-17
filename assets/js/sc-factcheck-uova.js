/* S-COMODO | Interazioni editoriali senza tracker e senza richieste esterne. */
(function () {
  "use strict";
  function setupExplorer(root) {
    var bar = root.querySelector("[data-fc-filters]");
    var items = Array.prototype.slice.call(root.querySelectorAll("[data-status]"));
    var count = root.querySelector("[data-fc-count]");
    if (!bar || !items.length) return;
    bar.hidden = false;
    var choices = Array.prototype.slice.call(bar.querySelectorAll("button[data-fc-filter]"));
    function choose(filter) {
      var visible = 0;
      items.forEach(function (card) {
        var show = filter === "tutti" || card.dataset.status === filter;
        card.hidden = !show;
        if (show) visible += 1;
      });
      choices.forEach(function (button) {
        button.setAttribute("aria-pressed", String(button.dataset.fcFilter === filter));
      });
      if (count) count.textContent = visible + (visible === 1 ? " affermazione visualizzata" : " affermazioni visualizzate") + " · Apri una scheda per leggere le verifiche";
    }
    bar.addEventListener("click", function (event) {
      var choice = event.target.closest("button[data-fc-filter]");
      if (choice && bar.contains(choice)) choose(choice.dataset.fcFilter);
    });
    choose("tutti");
  }
  function setupMethod(root) {
    var controls = root.querySelector("[data-fc-stages]");
    var panel = root.querySelector("[data-fc-method-panel]");
    if (!controls || !panel) return;
    var label = panel.querySelector("[data-fc-method-title]");
    var detail = panel.querySelector("[data-fc-method-text]");
    var stages = [
      ["Il materiale di partenza", "Testimonianze, documenti e riprese sono indizi o evidenze di eventi specifici. Occorre conoscere data, luogo, provenienza, integrità e limiti di ciascuna fonte."],
      ["La verifica indipendente", "Un secondo riscontro autonomo, registri originali, controlli ufficiali o analisi ripetibili permettono di valutare se un fatto sia stato confermato anche fuori dalla narrazione televisiva."],
      ["Il contraddittorio", "La parte coinvolta deve conoscere contestazioni sufficientemente specifiche e poter replicare. Una risposta evasiva non prova un illecito; una smentita non cancella prove indipendenti."],
      ["La conclusione proporzionata", "Distinguere episodio e sistema, correlazione e causalità, comportamento contestato e responsabilità accertata. Dichiarare ciò che resta ignoto e correggere eventuali errori."]
    ];
    var buttons = Array.prototype.slice.call(controls.querySelectorAll("button[data-fc-stage]"));
    function select(index) {
      if (!stages[index]) return;
      if (label) label.textContent = stages[index][0];
      if (detail) detail.textContent = stages[index][1];
      buttons.forEach(function (button) {
        button.setAttribute("aria-pressed", String(Number(button.dataset.fcStage) === index));
      });
    }
    controls.hidden = false;
    controls.addEventListener("click", function (event) {
      var button = event.target.closest("button[data-fc-stage]");
      if (button && controls.contains(button)) select(Number(button.dataset.fcStage));
    });
    select(0);
  }
  function initialize() {
    document.querySelectorAll("[data-fc-explorer]").forEach(setupExplorer);
    document.querySelectorAll("[data-fc-method]").forEach(setupMethod);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
  else initialize();
})();