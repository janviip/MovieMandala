// Fake movie data (use this until backend is ready)
const fakeMovies = [
  { title: "The Dark Knight",  genre: "Action · Crime"    },
  { title: "Interstellar",     genre: "Sci-Fi · Drama"    },
  { title: "The Prestige",     genre: "Mystery · Thriller"},
  { title: "Memento",          genre: "Thriller · Mystery"},
  { title: "Shutter Island",   genre: "Thriller · Drama"  },
  { title: "Tenet",            genre: "Sci-Fi · Action"   },
  { title: "Arrival",          genre: "Sci-Fi · Drama"    },
  { title: "Looper",           genre: "Sci-Fi · Action"   },
  { title: "The Matrix",       genre: "Sci-Fi · Action"   },
  { title: "Parasite",         genre: "Thriller · Drama"  },
];

function searchMovie() {
  const input = document.getElementById('searchInput').value.trim();

  // if empty, do nothing
  if (!input) {
    alert('Please enter a movie name!');
    return;
  }

  // hide default message
  document.getElementById('defaultMessage').classList.add('hidden');

  // show loading spinner
  const container = document.getElementById('resultsContainer');
  container.classList.remove('hidden');
  container.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Finding similar movies...</p>
    </div>
  `;

  // simulate waiting for backend (1.5 seconds)
  setTimeout(() => {
    showResults(input, fakeMovies);
  }, 1500);

  // -------------------------------------------------
  // LATER: replace the setTimeout above with this
  // when your teammates finish the backend:
  //
  // fetch(`http://localhost:5000/recommend?movie=${input}`)
  //   .then(res => res.json())
  //   .then(data => showResults(input, data.recommendations))
  //   .catch(() => showError());
  // -------------------------------------------------
}

function showResults(movieName, movies) {
  const container = document.getElementById('resultsContainer');

  const cards = movies.map(movie => `
    <div class="movie-card">
      <div class="no-poster">🎬</div>
      <div class="card-info">
        <div class="card-title">${movie.title}</div>
        <div class="card-genre">${movie.genre}</div>
      </div>
    </div>
  `).join('');

  container.innerHTML = `
    <h3 class="results-title">
      Recommended movies for: <span>${movieName}</span>
    </h3>
    <div class="movies-grid">${cards}</div>
  `;
}

function showError() {
  const container = document.getElementById('resultsContainer');
  container.innerHTML = `
    <div class="error-msg">
      ❌ Could not find recommendations. Please try again.
    </div>
  `;
}

// allow pressing Enter key to search
document.getElementById('searchInput')
  .addEventListener('keypress', function(e) {
    if (e.key === 'Enter') searchMovie();
  });