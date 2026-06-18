const fakeMovies = [
  { title: "Movie name" },
  { title: "Movie name" },
  { title: "Movie name" },
  { title: "Movie name" },
  { title: "Movie name" },
];

function renderMovies(movies) {
  const grid = document.getElementById('moviesGrid');
  grid.innerHTML = movies.map(m => `
    <div class="movie-slot">
      <div class="name">${m.title}</div>
      <div class="poster-box">
        <!-- placeholder box like the wireframe; later this becomes <img src="poster_url"> -->
      </div>
    </div>
  `).join('');
}

function searchMovie() {
  const input = document.getElementById('searchInput').value.trim();
  if (!input) {
    alert('Please enter a movie name!');
    return;
  }
  renderMovies(fakeMovies);
}

// show 5 placeholder cards when page first loads
renderMovies(fakeMovies);