/* Reading aids only: article copy and citations remain untouched. */
(()=>{'use strict';
 const article=document.querySelector('article.article');if(!article)return;
 const body=article.querySelector('.article-body'),index=article.querySelector('.reading-index');if(!body||!index)return;
 const lang=document.documentElement.lang;
 const labels=lang==='es'?{contents:'En este artículo'}:lang==='en'?{contents:'In this article'}:{contents:'In questo articolo'};
 const headings=[...body.querySelectorAll('h2')].filter(h=>h.textContent.trim());
 if(headings.length>=3){
  const details=document.createElement('details'),summary=document.createElement('summary'),list=document.createElement('ol');
  summary.textContent=labels.contents;details.open=matchMedia('(min-width:1101px)').matches;
  headings.forEach((h,i)=>{if(!h.id)h.id='reading-section-'+(i+1);const li=document.createElement('li'),a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;li.append(a);list.append(li)});
  details.append(summary,list);index.append(details);index.hidden=false;
  list.addEventListener('click',event=>{if(event.target.closest('a')&&matchMedia('(max-width:1100px)').matches)details.open=false});
 }
 const meter=document.createElement('div');meter.className='reading-progress';meter.setAttribute('aria-hidden','true');document.body.append(meter);
 let scheduled=false;
 function draw(){const rect=body.getBoundingClientRect(),distance=Math.max(1,body.offsetHeight-innerHeight);const fraction=Math.max(0,Math.min(1,-rect.top/distance));meter.style.transform='scaleX('+fraction+')';scheduled=false}
 addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(draw)}},{passive:true});addEventListener('resize',draw);draw();
 // Tables keep every column, scrolling locally on narrow screens.
 body.querySelectorAll('table').forEach(table=>{
  const wrap=document.createElement('div'),hint=document.createElement('p');
  wrap.className='reading-table';wrap.tabIndex=0;wrap.setAttribute('role','region');wrap.setAttribute('aria-label',lang==='es'?'Tabla desplazable':lang==='en'?'Scrollable table':'Tabella scorrevole');
  hint.className='reading-table-hint';hint.textContent=lang==='es'?'Desliza para leer toda la tabla ↔':lang==='en'?'Scroll to read the full table ↔':'Scorri per leggere tutta la tabella ↔';
  table.before(hint,wrap);wrap.append(table);
  const update=()=>{hint.hidden=table.scrollWidth<=wrap.clientWidth+1};
  if('ResizeObserver' in window)new ResizeObserver(update).observe(wrap);update();
 });
})();
