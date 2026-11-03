(function () {
"use strict";
const root=document.getElementById("sc015-lab");
if(!root)return;
const quizData=[
{q:"Un amico ti manda una notizia clamorosa. Che fai?",choices:["La condivido subito. È troppo importante.","Cerco la fonte originale e verifico il contenuto.","Aspetto prima di condividerla, anche se mi sembra credibile."],points:[0,2,1]},
{q:"Qualcuno dimostra che un'affermazione che hai fatto è sbagliata.",choices:["Esamino la dimostrazione e, se è convincente, mi correggo.","Cerco di salvare almeno una parte della mia argomentazione.","Preferisco non continuare la discussione."],points:[2,0,1]},
{q:"Durante una cena si parla di un argomento che non conosci.",choices:["Ripeto qualcosa che ho sentito dire da un esperto.","Ascolto, senza necessariamente intervenire.","Dico che non lo conosco e faccio domande."],points:[0,1,2]},
{q:"Avevi previsto con sicurezza un risultato. È accaduto il contrario.",choices:["Riconosco l'errore e cerco di capire perché la previsione non ha funzionato.","Sostengo che, in fondo, avevo ragione lo stesso.","Evito di discutere della previsione precedente."],points:[2,0,1]},
{q:"Trovi uno studio che conferma perfettamente le tue idee.",choices:["Lo condivido: la scienza mi dà ragione!","Lo conservo e mi riprometto di approfondirlo.","Controllo come è stato condotto, quali limiti presenta e se esistono altre ricerche."],points:[0,1,2]},
{q:"Ti chiedono di spiegare nel dettaglio qualcosa che credi di conoscere. Ti accorgi di non saperlo fare.",choices:["Improvviso una spiegazione plausibile.","Ammetto di non conoscerlo abbastanza e cerco di approfondire.","Chiedo se qualcun altro può spiegare meglio."],points:[0,2,1]},
{q:"Una persona con cui sei spesso in disaccordo presenta un argomento convincente.",choices:["Lo riconosco e considero se modificare la mia posizione.","Ricordo immediatamente le altre occasioni in cui ha sbagliato.","Ammetto che l'argomento è interessante, ma resto prudente."],points:[2,0,1]},
{q:"Hai ottenuto un punteggio elevato in questo test. Qual è il primo pensiero?",choices:["Lo sapevo. Sono superiore alla media.","È un gioco divertente, ma non dimostra quanto sono intelligente.","Lo condivido per scherzare con gli amici."],points:[0,2,1]}
];
const form=root.querySelector("#sc015-quiz-form");
const results=root.querySelector("#sc015-quiz-results");
quizData.forEach((item,i)=>{
 const set=document.createElement("fieldset");set.className="lab-question";
 const leg=document.createElement("legend");leg.textContent=(i+1)+". "+item.q;set.appendChild(leg);
 item.choices.forEach((choice,j)=>{
 const label=document.createElement("label");label.className="lab-option";
 const input=document.createElement("input");input.type="radio";input.name="sc015-q"+i;input.value=String(j);input.required=true;
 const span=document.createElement("span");span.textContent=String.fromCharCode(65+j)+". "+choice;
 label.append(input,span);set.appendChild(label);
 });
 form.insertBefore(set,form.querySelector('.lab-buttons'));
});
form.addEventListener("submit",function(e){
 e.preventDefault();
 if(!form.reportValidity())return;
 let score=0;quizData.forEach((item,i)=>{const a=form.querySelector('input[name="sc015-q'+i+'"]:checked');score+=item.points[Number(a.value)];});
 const labels=[
 ["La sirena delle certezze","La risposta arriva prima della domanda. Prova a verificare una convinzione prima di difenderla."],
 ["Il tuttologo in manutenzione","Qualche buon dubbio, ma talvolta il bisogno di avere ragione prende il volante. Lascia guidare anche le prove."],
 ["Cervello con revisione attiva","Mostri disponibilità ad ascoltare e verificare. Non farne un nuovo motivo per sentirti superiore."],
 ["Il saggio provvisorio","Hai scelto spesso le risposte più riflessive. Ma sono soltanto otto domande editoriali, non un dottorato in saggezza."]
 ];
 const b=score<=4?0:score<=9?1:score<=13?2:3;
 results.replaceChildren();
 const heading=document.createElement("strong");heading.textContent=labels[b][0]+" — "+score+"/16";
 const p=document.createElement("p");p.textContent=labels[b][1]+" Il punteggio è puramente ludico, non una misura psicologica.";
 results.append(heading,p);results.hidden=false;results.focus();
});
root.querySelector("#sc015-quiz-reset").addEventListener("click",()=>{form.reset();results.hidden=true;results.replaceChildren()});
const words=[
{n:1,word:"CERTEZZA",r:0,c:9,dir:"v",clue:"Quando diventa assoluta e immotivata, rischia di accecarci (8)"},
{n:2,word:"SAGGEZZA",r:1,c:0,dir:"h",clue:"Non è sinonimo di QI né una medaglia permanente (8)"},
{n:3,word:"ASCOLTO",r:1,c:7,dir:"v",clue:"È utile prima di rispondere a chi la pensa diversamente (7)"},
{n:4,word:"DUBBIO",r:4,c:2,dir:"h",clue:"Fa spazio alle domande prima di distribuire sentenze (6)"},
{n:5,word:"UMILTA",r:4,c:3,dir:"v",clue:"Ci aiuta ad ammettere che possiamo sbagliarci (6)"},
{n:6,word:"ERRORE",r:5,c:1,dir:"v",clue:"Ammetterlo sembra uno sport estremo per certi tuttologi (6)"},
{n:7,word:"PROVA",r:7,c:5,dir:"h",clue:"Sostiene un'affermazione più del volume della voce (5)"},
{n:8,word:"FONTE",r:8,c:0,dir:"h",clue:"Andrebbe controllata prima di condividere una notizia (5)"}
];
const grid=root.querySelector("#sc015-crossword-grid");
const clueH=root.querySelector("#sc015-clues-h");
const clueV=root.querySelector("#sc015-clues-v");
const live=root.querySelector("#sc015-crossword-status");
const entries=new Map(), membership=new Map(), starts=new Map();let active=null;
const key=(r,c)=>r+","+c;
words.forEach(w=>{
 w.cells=[];
 [...w.word].forEach((letter,i)=>{const r=w.r+(w.dir==="v"?i:0),c=w.c+(w.dir==="h"?i:0),k=key(r,c);
 if(entries.has(k)&&entries.get(k)!==letter)throw Error("Contradizione griglia "+k);
 entries.set(k,letter);w.cells.push(k);
 const m=membership.get(k)||[];m.push(w);membership.set(k,m);
 });
 starts.set(key(w.r,w.c),w.n);
});
const nodes=new Map();
for(let r=0;r<11;r++)for(let c=0;c<10;c++){
 const k=key(r,c),cell=document.createElement("div");cell.className="crossword-cell";
 if(!entries.has(k)){cell.classList.add("block");cell.setAttribute("aria-hidden","true");grid.appendChild(cell);continue}
 const num=starts.get(k);
 if(num){const badge=document.createElement("span");badge.className="crossword-number";badge.textContent=String(num);cell.appendChild(badge)}
 const input=document.createElement("input");input.type="text";input.maxLength=1;input.autocomplete="off";input.spellcheck=false;input.autocapitalize="characters";input.inputMode="text";
 input.setAttribute("aria-label","Casella riga "+(r+1)+", colonna "+(c+1)+(num?", parola "+num:""));
 input.dataset.cell=k;
 cell.appendChild(input);grid.appendChild(cell);nodes.set(k,{cell,input,r,c});
 input.addEventListener("focus",()=>{const members=membership.get(k);if(!active||!members.includes(active))setActive(members[0])});
 input.addEventListener("click",()=>{const members=membership.get(k);if(members.length>1&&active&&members.includes(active)){setActive(members[(members.indexOf(active)+1)%members.length]);}});
 input.addEventListener("input",()=>{
  const clean=input.value.toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^A-Z]/g,"").slice(-1);
  input.value=clean;cell.classList.remove("error");live.textContent="";
  if(clean&&active){const i=active.cells.indexOf(k);const next=active.cells[i+1];if(next)nodes.get(next).input.focus()}
 });
 input.addEventListener("keydown",e=>{
  if(e.key==="Backspace"&&!input.value&&active){const p=active.cells[active.cells.indexOf(k)-1];if(p){nodes.get(p).input.value="";nodes.get(p).input.focus();e.preventDefault()}}
  const moves={ArrowLeft:[r,c-1],ArrowRight:[r,c+1],ArrowUp:[r-1,c],ArrowDown:[r+1,c]};
  if(moves[e.key]){const target=nodes.get(key(...moves[e.key]));if(target){target.input.focus();e.preventDefault()}}
 });
}
function setActive(w){
 active=w;for(const [k,n]of nodes)n.cell.classList.toggle("active",w.cells.includes(k));
 root.querySelectorAll(".clue-button").forEach(b=>b.setAttribute("aria-pressed",String(Number(b.dataset.word)===w.n)));
}
words.forEach(w=>{
 const li=document.createElement("li"),btn=document.createElement("button");btn.type="button";btn.className="clue-button";btn.dataset.word=String(w.n);btn.setAttribute("aria-pressed","false");btn.textContent=w.n+". "+w.clue;
 btn.addEventListener("click",()=>{setActive(w);nodes.get(w.cells[0]).input.focus()});li.appendChild(btn);
 (w.dir==="h"?clueH:clueV).appendChild(li);
});
root.querySelector("#sc015-check-crossword").addEventListener("click",()=>{
 let correct=0,filled=0;
 for(const [k,n]of nodes){const value=n.input.value.toUpperCase();if(value)filled++;if(value===entries.get(k))correct++;n.cell.classList.toggle("error",Boolean(value&&value!==entries.get(k)))}
 live.textContent=correct===nodes.size?"Complimenti! Cruciverba completato correttamente.":correct+" lettere corrette su "+nodes.size+". Caselle compilate: "+filled+". Le lettere errate sono evidenziate.";
});
root.querySelector("#sc015-clear-crossword").addEventListener("click",()=>{for(const n of nodes.values()){n.input.value="";n.cell.classList.remove("error")}live.textContent="Griglia ricominciata.";if(active)nodes.get(active.cells[0]).input.focus()});
root.querySelector("#sc015-reveal-crossword").addEventListener("click",()=>{for(const [k,n]of nodes){n.input.value=entries.get(k);n.cell.classList.remove("error")}live.textContent="Soluzioni visualizzate. Non è più possibile controllare il proprio tentativo senza ricominciare."});
})();