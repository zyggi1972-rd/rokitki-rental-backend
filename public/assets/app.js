document.addEventListener('DOMContentLoaded', ()=>{
  const search = document.getElementById('search');
  const typeahead = document.getElementById('typeahead');
  if(search && typeahead){
    let timer;
    search.addEventListener('input', ()=>{
      clearTimeout(timer);
      const q = search.value.trim();
      if(q.length < 2){ typeahead.classList.add('d-none'); return; }
      timer = setTimeout(async ()=>{
        try{
          const res = await fetch('/api/search?q=' + encodeURIComponent(q));
          if(!res.ok) throw new Error('net');
          const items = await res.json();
          typeahead.innerHTML = items.map(i=>`<a href="/offers/${i.slug}" class="list-group-item list-group-item-action">${i.title}</a>`).join('');
          typeahead.classList.toggle('d-none', items.length===0);
        }catch(e){ typeahead.classList.add('d-none'); }
      }, 200);
    });
  }
});

