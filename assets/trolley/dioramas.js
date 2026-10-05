// One host for every diorama on the page, registered before the first frame so no first message is missed;
// the 1.6 MB of results loads once, when the first pane asks for it
(()=>{
  const st=new Map(),waiting=[];let loading=false;
  const figs=()=>[...document.querySelectorAll('figure.dio')];
  const state=f=>{if(!st.has(f)){const [scenario,model,n,w,o]=f.dataset.preset.split('|');st.set(f,{scenario,model,n,w,o,shown:null,marks:[]})}return st.get(f)};
  const post=(f,m)=>f.querySelector('iframe').contentWindow.postMessage(m,'*');
  // A new setup starts on its first wording, as the controls expect; the track order carries over
  const firstWording=id=>{const sc=window.DIO_DATA&&window.DIO_DATA.scenarios.find(x=>x.id===id);return sc?sc.wordings[0].id:'v1'};
  const preset=f=>{const s=state(f);post(f,{type:'dio-preset',spec:[s.scenario,s.model,s.n,s.w||firstWording(s.scenario),s.o||'o1'].join('|'),compare:false})};
  const give=f=>{
    if(window.DIO_DATA)return post(f,{type:'dio-data',data:window.DIO_DATA});
    waiting.push(f);if(loading)return;loading=true;
    const js=document.createElement('script');js.src='/assets/trolley/results.js';js.onload=()=>waiting.splice(0).forEach(give);document.head.append(js);
  };

  // What changed since the last question, marked in the prompt so switching setups shows the difference.
  // From the article: a word-level diff finds what changed, and only the words that carry the meaning of the change
  // are marked, a changed count and the word that names what sits on the side track. When most of the prompt changed
  // (another wording, another family of setups) nothing is marked, and a pure reorder marks nothing either.
  // A figure's first question is compared with the question the figure before it opens on, so the page reads in order
  const MARK_MAX=0.45;
  const KEY_PHRASES=[/\bstranger\b/i,/\bengineers?\b/i,/\bserver\b/i];
  const NUMBER_WORDS='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split(' ');
  const countValue=w=>/^\d+$/.test(w)?+w:NUMBER_WORDS.indexOf(w.toLowerCase());
  const bareWord=w=>(w||'').replace(/^["“(]+|[.,;:)"”]+$/g,'');
  const countsIn=ws=>ws.map((w,i)=>countValue(bareWord(w))>=0&&/^(?:people|person)$/i.test(bareWord(ws[i+1]))?countValue(bareWord(w)):-1);
  const tokens=full=>full.split(/(\s+)/);
  const wordsOf=full=>tokens(full).filter((x,i)=>i%2===0&&x);
  const changedWords=(a,b)=>{
    const n=a.length,m=b.length,dp=Array.from({length:n+1},()=>new Uint16Array(m+1));
    for(let i=n-1;i>=0;i--)for(let j=m-1;j>=0;j--)dp[i][j]=a[i]===b[j]?dp[i+1][j+1]+1:Math.max(dp[i+1][j],dp[i][j+1]);
    const changed=new Array(m).fill(true);
    for(let i=0,j=0;i<n&&j<m;){if(a[i]===b[j]){changed[j]=false;i++;j++}else if(dp[i+1][j]>=dp[i][j+1])i++;else j++}
    return changed;
  };
  // Counts are compared slot by slot (main track, side track, then who is killed); when the two questions hold
  // different numbers of counts the slots do not line up and the side-track word carries the change
  const keyWords=(full,changed,prev)=>{
    const spans=[];let at=0;
    tokens(full).forEach((t,i)=>{if(i%2===0&&t)spans.push([at,at+t.length]);at+=t.length});
    const marked=new Set(),before=countsIn(wordsOf(prev)).filter(v=>v>=0),now=countsIn(wordsOf(full)),counted=new Set();
    if(before.length===now.filter(v=>v>=0).length){let nth=0;now.forEach((v,i)=>{if(v<0)return;const was=before[nth++];if(was===v||!changed[i]||counted.has(v))return;marked.add(i);counted.add(v)})}
    for(const re of KEY_PHRASES){
      const m=re.exec(full);if(!m||re.test(prev))continue;
      const inPhrase=spans.map(([a,b],i)=>a<m.index+m[0].length&&b>m.index?i:-1).filter(i=>i>=0);
      if(inPhrase.some(i=>changed[i]))inPhrase.forEach(i=>marked.add(i));
    }
    return [...marked].sort((x,y)=>x-y);
  };
  const marksFor=(full,prev)=>{
    if(!prev||prev===full)return [];
    const before=wordsOf(prev),now=wordsOf(full),ch=changedWords(before,now),k=ch.filter(Boolean).length;
    const reorder=before.length===now.length&&[...before].sort().join(' ')===[...now].sort().join(' ');
    return k&&k/ch.length<=MARK_MAX&&!reorder?keyWords(full,ch,prev):[];
  };
  // The question the figure before this one opens on, from its preset
  const openingBefore=f=>{
    const all=figs(),i=all.indexOf(f),D=window.DIO_DATA;if(i<1||!D)return null;
    const [scenario,,n,w,o]=all[i-1].dataset.preset.split('|');
    const t=D.texts[[scenario,w||'v1',o||'o1',n].join('|')];return t?t.state:null;
  };

  // The pane posts the exact prompt on every setup change; the page sets it in its own type
  const quote=(f,d)=>{
    const q=f.querySelector('.dio-q');if(!q)return;
    const s=state(f),t=q.querySelector('.dio-q-text');
    if(d.text!==s.shown){s.marks=d.ok?marksFor(d.text,s.shown===null?openingBefore(f):s.shown):[];s.shown=d.text}
    t.dataset.full=d.text;t.classList.toggle('json',!!d.json);
    q.querySelector('.dio-q-ask').textContent=d.q;
    q.querySelectorAll('.dio-q-who').forEach(e=>e.textContent=d.model);
    const sel=f.querySelector('select[name=wording]');
    if(sel)sel.replaceChildren(...d.wordings.map(w=>{const o=new Option(w.label+(w.ok?'':' (not run for '+d.model+')'),w.id,false,w.id===d.wording);o.disabled=!w.ok;return o}));
    const ord=f.querySelector('input[name=order]');
    // Ticked, the other part of the scene comes first: the side track, or on the push the footbridge
    if(ord){ord.checked=d.order==='o2';ord.nextElementSibling.textContent=/^the (footbridge|track)$/.test(d.first)?'Footbridge described first':'Side track described first'}
    q.classList.remove('open');cap(f);
  };
  // Words from..to of the prompt, its own spacing kept, the changed words wrapped in <mark>
  const renderWords=(f,full,from,to)=>{
    const marked=new Set(state(f).marks),tk=tokens(full),frag=document.createDocumentFragment();
    let w=-1,run=null;
    for(let i=0;i<tk.length;i++){
      const isWord=i%2===0;
      if(isWord){if(!tk[i])continue;w++}
      if(w<from||w>=to||(!isWord&&w===to-1))continue;
      if(isWord&&marked.has(w)){
        let word=tk[i];
        if(!run){const lead=word.match(/^["“(]+/);if(lead){frag.append(lead[0]);word=word.slice(lead[0].length)}run=document.createElement('mark');run.className='kw';frag.append(run)}
        const end=!marked.has(w+1)||w+1>=to,trail=end&&word.match(/[.,;:!?)"”]+$/);
        run.append(trail?word.slice(0,-trail[0].length):word);if(trail)frag.append(trail[0]);if(end)run=null;
      }else if(!isWord&&run)run.append(tk[i]);else frag.append(tk[i]);
    }
    return frag;
  };
  const showWords=(f,t,from,to,n)=>{
    const frag=renderWords(f,t.dataset.full,from,to);
    if(to<n){const last=frag.lastChild;if(last&&last.nodeType===3)last.textContent=last.textContent.replace(/[\s,;:]+$/,'');frag.append('…')}
    if(from>0)frag.prepend('…');
    t.replaceChildren(frag);
  };
  // A prompt longer than its cap folds to its first lines until the reader asks for the rest
  const cap=f=>{
    const q=f.querySelector('.dio-q'),b=q&&q.querySelector('.dio-q-more');
    // A pane that has not loaded yet has no prompt to fold; its first quote calls this again
    if(b&&q.querySelector('.dio-q-text').dataset.full!==undefined){
      const t=q.querySelector('.dio-q-text'),open=q.classList.contains('open'),n=wordsOf(t.dataset.full||'').length;
      const apply=()=>{
        q.classList.remove('open');q.classList.add('long');showWords(f,t,0,n,n);
        const long=t.scrollHeight>t.clientHeight+2;
        q.classList.toggle('long',long);q.classList.toggle('open',open&&long);
        if(long&&!open)fold(f,t);else srCopy(f,t,true);
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
  // Screen readers get the whole prompt, and what changed in it
  const srCopy=(f,t,whole)=>{
    const full=t.dataset.full,w=wordsOf(full),runs=[],marks=state(f).marks;
    marks.forEach((i,x)=>{if(x&&marks[x-1]===i-1)runs[runs.length-1].push(w[i]);else runs.push([w[i]])});
    const said=runs.length?` Changed from the previous question: ${runs.map(r=>r.join(' ')).join('; ')}.`:'';
    if(whole){if(said){const sr=document.createElement('span');sr.className='dio-q-sr';sr.textContent=said;t.append(sr)}return}
    const vis=document.createElement('span'),sr=document.createElement('span');
    vis.append(...t.childNodes);vis.setAttribute('aria-hidden','true');sr.className='dio-q-sr';sr.textContent=full+said;t.replaceChildren(vis,sr);
  };
  // The browser's own clamp ends the last line mid-word; this keeps whole words and puts the ellipsis after them.
  // When part of the change falls past the fold, the excerpt starts at the sentence the change starts in
  const fold=(f,t)=>{
    const full=t.dataset.full,n=wordsOf(full).length;
    const most=from=>{const fits=k=>{showWords(f,t,from,from+k,n);return t.scrollHeight<=t.clientHeight+1};let lo=1,hi=n-from-1;while(lo<hi){const m=(lo+hi+1)>>1;if(fits(m))lo=m;else hi=m-1}return lo};
    let from=0,k=most(0);
    const marks=state(f).marks,seen=(a,c)=>marks.filter(i=>i>=a&&i<a+c).length;
    if(marks.length&&marks[marks.length-1]>=k){
      const w=wordsOf(full);let s=marks[0];while(s>0&&!/[.;:!?]$/.test(w[s-1]))s--;
      const k2=most(s);if(seen(s,k2)>seen(0,k)){from=s;k=k2}
    }
    showWords(f,t,from,from+k,n);srCopy(f,t,false);
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
    // The compact setup select and the setup chips are one control at two widths, so each follows the other
    if(e.target.name==='scenario'){s.scenario=e.target.value;s.w='';f.querySelectorAll('[data-scenario]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.scenario===e.target.value));preset(f)}
  });
  document.addEventListener('click',e=>{const b=e.target.closest('figure.dio [data-scenario]'),sel=b&&b.closest('figure.dio').querySelector('select[name=scenario]');if(sel)sel.value=b.dataset.scenario});
  document.addEventListener('click',e=>{const b=e.target.closest('.dio-q-more');if(!b)return;const f=b.closest('figure.dio');f.querySelector('.dio-q').classList.toggle('open');cap(f)});
  // A details fold changes the figure's height, so the scene refits
  document.addEventListener('toggle',e=>{const f=e.target.closest&&e.target.closest('figure.dio');if(f)fit(f)},true);
})();
