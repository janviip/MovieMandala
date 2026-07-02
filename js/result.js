const englishMovies = ["Inception", "The Dark Knight", "Interstellar", "Avatar", "Avengers"];
const horrorMovies = ["The Conjuring", "Hereditary", "It", "Insidious", "Sinister"];
const romanticMovies = ["Titanic", "The Notebook", "La La Land", "About Time", "Me Before You"];

const fakeResults = ["The Prestige", "Memento", "Shutter Island", "Tenet", "Arrival"];

function renderRow(containerId, movies) {
  const container = document.getElementById(containerId);
  container.innerHTML = movies.map(title => `
    <div class="poster-card">
      <div class="poster-box">No poster</div>
      <div class="poster-name">${title}</div>
    </div>
  `).join('');
}

function searchMovie() {
  const input = document.getElementById('searchInput').value.trim();
  if (!input) {
    alert('Please enter a movie name!');
    return;
  }
  document.getElementById('searchResultsSection').style.display = 'block';
  renderRow('resultsRow', fakeResults);
}

renderRow('englishRow', englishMovies);
renderRow('horrorRow', horrorMovies);
renderRow('romanticRow', romanticMovies);