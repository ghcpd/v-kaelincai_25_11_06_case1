document.getElementById('searchBtn').addEventListener('click', async ()=>{
  const q = document.getElementById('q').value;
  const res = await fetch(`/search?q=${encodeURIComponent(q)}`);
  const json = await res.json();
  const ul = document.getElementById('results');
  ul.innerHTML = '';
  for (const item of json.results){
    const li = document.createElement('li');
    li.textContent = `${item.name} (score=${item.score.toFixed(2)})`;
    ul.appendChild(li);
  }
});
