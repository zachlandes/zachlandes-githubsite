// One host for every diorama on the page, registered before the first frame so no first message is missed;
// the 1.6 MB of results loads once, when the first pane asks for it
(()=>{
  const st=new Map(),waiting=[];let loading=false;
  const figs=()=>[...document.querySelectorAll('figure.dio')];
  const state=f=>{if(!st.has(f)){const [scenario,model,n,w,o]=f.dataset.preset.split('|');st.set(f,{scenario,model,n,w,o})}return st.get(f)};
  const post=(f,m)=>f.querySelector('iframe').contentWindow.postMessage(m,'*');
  // A new setup starts on its first wording, as the controls expect; the track order carries over
  const firstWording=id=>{const sc=window.DIO_DATA&&window.DIO_DATA.scenarios.find(x=>x.id===id);return sc?sc.wordings[0].id:'v1'};
  const preset=f=>{const s=state(f);post(f,{type:'dio-preset',spec:[s.scenario,s.model,s.n,s.w||firstWording(s.scenario),s.o||'o1'].join('|'),compare:false})};
  const give=f=>{
    if(window.DIO_DATA)return post(f,{type:'dio-data',data:window.DIO_DATA});
    waiting.push(f);if(loading)return;loading=true;
    const js=document.createElement('script');js.src='/assets/trolley/results.js';js.onload=()=>waiting.splice(0).forEach(give);document.head.append(js);
  };

  const tokens=full=>full.split(/(\s+)/);
  const wordsOf=full=>tokens(full).filter((x,i)=>i%2===0&&x);

  // The pane posts the exact prompt on every setup change; the page sets it in its own type
  const quote=(f,d)=>{
    const q=f.querySelector('.dio-q');if(!q)return;
    const t=q.querySelector('.dio-q-text');
    t.dataset.full=d.text;t.classList.toggle('json',!!d.json);
    q.querySelector('.dio-q-ask').textContent=d.q;
    q.querySelectorAll('.dio-q-who').forEach(e=>e.textContent=d.model);
    const sel=f.querySelector('select[name=wording]');
    if(sel)sel.replaceChildren(...d.wordings.map(w=>{const o=new Option(w.label+(w.ok?'':' (not run for '+d.model+')'),w.id,false,w.id===d.wording);o.disabled=!w.ok;return o}));
    const ord=f.querySelector('input[name=order]');
    // Ticked, the other part of the scene comes first: the side track, or on the push the footbridge
    if(ord){ord.checked=d.order==='o2';ord.nextElementSibling.textContent=/^the (footbridge|track)$/.test(d.first)?'Footbridge described first':'Side track described first'}
    // Each setup was asked at its own crowd sizes; the count controls offer only those
    if(d.ns){
      const n=Number(d.n),cnt=f.querySelector('select[name=count]');
      if(cnt)cnt.replaceChildren(...d.ns.map(x=>new Option(x,x,false,x===n)));
      f.querySelectorAll('[data-n]').forEach(b=>{b.disabled=!d.ns.includes(Number(b.dataset.n));b.setAttribute('aria-pressed',String(Number(b.dataset.n)===n))});
    }
    q.classList.remove('open');cap(f);
  };
  // The prompt's first k words, its own spacing kept, with an ellipsis when that cuts it short
  const showWords=(t,k)=>{
    const tk=tokens(t.dataset.full);let w=0,text='';
    for(let i=0;i<tk.length&&w<k;i++){if(i%2===0){if(!tk[i])continue;w++}text+=tk[i]}
    t.textContent=w<wordsOf(t.dataset.full).length?text.replace(/[\s,;:]+$/,'')+'\u2026':text;
  };
  // A prompt longer than its cap folds to its first lines until the reader asks for the rest
  const cap=f=>{
    const q=f.querySelector('.dio-q'),b=q&&q.querySelector('.dio-q-more');
    // A pane that has not loaded yet has no prompt to fold; its first quote calls this again
    if(b&&q.querySelector('.dio-q-text').dataset.full!==undefined){
      const t=q.querySelector('.dio-q-text'),open=q.classList.contains('open'),n=wordsOf(t.dataset.full||'').length;
      const apply=()=>{
        q.classList.remove('open');q.classList.add('long');showWords(t,n);
        const long=t.scrollHeight>t.clientHeight+2;
        q.classList.toggle('long',long);q.classList.toggle('open',open&&long);
        if(long&&!open)fold(t);
        b.hidden=!long;b.textContent=open&&long?'Show less':'Show the full text';b.setAttribute('aria-expanded',open&&long);
      };
      q.style.removeProperty('--cap');apply();
      // Where a long sidenote above pushes the prompt down (the post script's --drop), it folds sooner so it still ends
      // with the scene's column instead of stretching the figure; taking it out of the grid for a moment measures that column
      if(parseFloat(q.style.getPropertyValue('--drop'))&&!open){
        q.style.position='absolute';
        const limit=Math.max(...[...f.children].filter(c=>c!==q).map(c=>c.getBoundingClientRect().bottom));
        q.style.position='';
        const line=parseFloat(getComputedStyle(t).lineHeight),over=q.getBoundingClientRect().bottom-limit;
        let c=Math.min(parseFloat(getComputedStyle(q).getPropertyValue('--cap')),Math.round(t.clientHeight/line)-Math.ceil(over/line));
        if(over>1)for(c=Math.max(3,c);;c--){q.style.setProperty('--cap',c);apply();if(c<=3||q.getBoundingClientRect().bottom<=limit+1)break}
      }
    }
    fit(f);
  };
  // The browser's own clamp ends the last line mid-word; this keeps whole words and puts the ellipsis after them,
  // with the full text still there for screen readers
  const fold=t=>{
    const full=t.dataset.full,n=wordsOf(full).length,fits=k=>{showWords(t,k);return t.scrollHeight<=t.clientHeight+1};
    let lo=1,hi=n-1;while(lo<hi){const m=(lo+hi+1)>>1;if(fits(m))lo=m;else hi=m-1}
    showWords(t,lo);
    const vis=document.createElement('span'),sr=document.createElement('span');
    vis.append(...t.childNodes);vis.setAttribute('aria-hidden','true');sr.className='dio-q-sr';sr.textContent=full;t.replaceChildren(vis,sr);
  };
  // Narrow the scene just enough that setup, prompt, scene and buttons share one screen; the figure's
  // CSS opts in with --fit:1 and sets the narrowest scene with --fit-min; sizes come from inside the pane, as the frame's own height lags a resize
  const fit=f=>{
    const i=f.querySelector('iframe'),doc=i.contentDocument,svg=doc&&doc.getElementById('stage-robot');
    if(getComputedStyle(f).getPropertyValue('--fit').trim()!=='1'){i.style.maxWidth='';return}
    const sr=svg&&svg.getBoundingClientRect();if(!sr||!sr.height)return;
    const fr=f.getBoundingClientRect(),ir=i.getBoundingClientRect(),ab=f.querySelector('.dio-actions').getBoundingClientRect().bottom;
    const paneH=doc.querySelector('.wrap').getBoundingClientRect().bottom+doc.defaultView.scrollY+8;
    const rest=ab-fr.top-ir.height,chrome=paneH-sr.height,padW=ir.width-sr.width,col=i.parentElement.getBoundingClientRect().width;
    const room=innerHeight-32-rest-chrome,min=parseFloat(getComputedStyle(f).getPropertyValue('--fit-min'))||400,w=Math.max(Math.min(col,min),Math.min(col,room*sr.width/sr.height+padW));
    const next=w>=col-1?'':Math.floor(w)+'px';if(i.style.maxWidth!==next)i.style.maxWidth=next;
  };
  addEventListener('resize',()=>figs().forEach(cap));
  document.addEventListener('margins',()=>figs().forEach(cap));
  addEventListener('message',e=>{
    const f=figs().find(x=>e.source===x.querySelector('iframe')?.contentWindow),d=e.data||{};
    if(!f)return;
    if(d.type==='dio-ready')give(f);
    // Auto keeps the pane on the reader's light or dark setting, as the page is
    if(d.type==='dio-loaded'){post(f,{type:'dio-theme',theme:'auto'});preset(f)}
    if(d.type==='dio-quote'){const s=state(f);if(d.ok){s.w=d.wording;s.o=d.order}quote(f,d)}
    if(d.type==='dio-height'){f.querySelector('iframe').style.height=Math.ceil(d.h)+4+'px';fit(f)}
  });
  document.addEventListener('click',e=>{
    const b=e.target.closest('figure.dio button');if(!b)return;
    const f=b.closest('figure.dio'),s=state(f);
    for(const k of ['scenario','n'])if(b.dataset[k]){s[k]=b.dataset[k];if(k==='scenario')s.w='';b.parentNode.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));preset(f)}
    if(b.dataset.act)post(f,{type:'dio-'+b.dataset.act});
  });
  document.addEventListener('change',e=>{
    const f=e.target.closest('figure.dio');if(!f)return;const s=state(f);
    if(e.target.name==='model'){s.model=e.target.value;preset(f)}
    if(e.target.name==='wording'){s.w=e.target.value;preset(f)}
    if(e.target.name==='order'){s.o=e.target.checked?'o2':'o1';preset(f)}
    if(e.target.name==='count'){s.n=e.target.value;preset(f)}
    // The compact setup select and the setup chips are one control at two widths, so each follows the other
    if(e.target.name==='scenario'){s.scenario=e.target.value;s.w='';f.querySelectorAll('[data-scenario]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.scenario===e.target.value));preset(f)}
  });
  document.addEventListener('click',e=>{const b=e.target.closest('figure.dio [data-scenario]'),sel=b&&b.closest('figure.dio').querySelector('select[name=scenario]');if(sel)sel.value=b.dataset.scenario});
  document.addEventListener('click',e=>{const b=e.target.closest('.dio-q-more');if(!b)return;const f=b.closest('figure.dio');f.querySelector('.dio-q').classList.toggle('open');cap(f)});
  // A details fold changes the figure's height, so the scene refits
  document.addEventListener('toggle',e=>{const f=e.target.closest&&e.target.closest('figure.dio');if(f)fit(f)},true);
})();
