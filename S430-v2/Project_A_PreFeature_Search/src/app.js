async function search() {
  const q = document.getElementById('q').value;
  const res = await fetch(`/search?query=${encodeURIComponent(q)}`);
  const json = await res.json();
  const ul = document.getElementById('results');
  ul.innerHTML = '';
  json.results.forEach(r => {
    const li = document.createElement('li');
    li.textContent = `${r.name} (score=${r.score}) (id=${r.id})`;
    ul.appendChild(li);
  });
}

document.getElementById('s').addEventListener('click', search);