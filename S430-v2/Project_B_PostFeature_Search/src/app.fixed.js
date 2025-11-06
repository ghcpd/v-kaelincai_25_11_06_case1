async function search() {
  const q = document.getElementById('q').value;
  const res = await fetch(`/search?query=${encodeURIComponent(q)}`);
  const json = await res.json();
  const ul = document.getElementById('results');
  ul.innerHTML = '';
  json.results.forEach(r => {
    const li = document.createElement('li');
    li.textContent = `${r.name} (score=${r.score}) (id=${r.id})`;
    if (r.recommendations) {
      li.textContent += ` -> recommendations: ${r.recommendations.map(rr => rr.name).join(', ')}`;
    }
    ul.appendChild(li);
  });
}

async function suggest() {
  const q = document.getElementById('q').value;
  const res = await fetch(`/suggest?q=${encodeURIComponent(q)}`);
  const json = await res.json();
  const ul = document.getElementById('suggestions');
  ul.innerHTML = '';
  json.suggestions.forEach(s => {
    const li = document.createElement('li');
    li.textContent = s;
    ul.appendChild(li);
  });
}

document.getElementById('s').addEventListener('click', search);
document.getElementById('g').addEventListener('click', suggest);
