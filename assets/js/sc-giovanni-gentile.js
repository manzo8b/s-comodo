/* S-COMODO | Lettura critica Gentile: nessun tracker, nessuna raccolta di dati */
(function(){
  "use strict";
  function init(){
    var root=document.querySelector("[data-scg]");if(!root)return;
    var filterbar=root.querySelector("[data-scg-filters]");
    if(filterbar){
      filterbar.hidden=false;
      var cards=Array.from(root.querySelectorAll(".scg-claim"));
      var choices=Array.from(filterbar.querySelectorAll("button[data-filter]"));
      function show(status){
        cards.forEach(function(card){card.hidden=status!=="all"&&card.dataset.kind!==status;});
        choices.forEach(function(b){b.setAttribute("aria-pressed",String(b.dataset.filter===status));});
      }
      filterbar.addEventListener("click",function(e){var b=e.target.closest("button[data-filter]");if(b&&filterbar.contains(b))show(b.dataset.filter);});
      show("all");
    }
    var reader=root.querySelector("[data-scg-reader]");
    if(!reader)return;
    var open=reader.querySelector("[data-scg-open]");
    var panel=reader.querySelector("[data-scg-reflection]");
    var title=reader.querySelector("[data-scg-reflection-title]");
    var copy=reader.querySelector("[data-scg-copy]");
    var note=reader.querySelector("#scg-comment");
    var feedback=reader.querySelector("[data-scg-feedback]");
    var interpretations={
      si:["Sì, con contestualizzazione","È possibile riconoscere un contributo filosofico senza aderire a tutte le idee dell'autore. La domanda critica è come evitare che la targa diventi una celebrazione acritica."],
      no:["No, per coerenza democratica","La denominazione di una strada è un riconoscimento civico. Si può conservare il ruolo di Gentile nello studio della filosofia senza conferirgli un omaggio pubblico."],
      cultura:["Soltanto in contesti culturali","Una biblioteca, un archivio o un percorso storico possono ricordare il pensiero di Gentile spiegandone anche il fascismo, senza trasformare la denominazione di una strada in un simbolo."],
      dipende:["Dipende dal contesto","Questa posizione richiede criteri controllabili: legame con il luogo, motivazione pubblica, biografia completa, partecipazione dei cittadini e possibili alternative."]
    };
    function current(){return reader.querySelector('input[name="scg-choice"]:checked');}
    function openReflection(){
      var selected=current();if(!selected)return;
      var x=interpretations[selected.value];if(!x)return;
      title.textContent=x[0];panel.querySelector("p").textContent=x[1];panel.hidden=false;
      if(feedback)feedback.textContent="Questa è una riflessione privata: nessun voto è stato registrato.";
    }
    if(open)open.addEventListener("click",openReflection);
    reader.querySelectorAll('input[name="scg-choice"]').forEach(function(r){r.addEventListener("change",function(){if(!panel.hidden)openReflection();});});
    if(copy)copy.addEventListener("click",function(){
      var selected=current();if(!selected)return;
      var label=interpretations[selected.value][0];
      var content="S-COMODO — Giovanni Gentile / una strada a suo nome\nPosizione: "+label+"\nMotivazione: "+(note?note.value.trim():"");
      if(navigator.clipboard&&navigator.clipboard.writeText){
        navigator.clipboard.writeText(content).then(function(){if(feedback)feedback.textContent="Riflessione copiata. Non è stata inviata né salvata dal sito.";}).catch(function(){if(feedback)feedback.textContent="Non è stato possibile copiare automaticamente. Puoi selezionare e copiare manualmente il testo.";});
      }else if(feedback){feedback.textContent="Copia manualmente il testo: il browser non consente la copia automatica.";}
    });
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();