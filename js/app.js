// Show a specific page (signup or login)
function showPage(pageName) {
  document.getElementById('signupPage').classList.add('hidden');
  document.getElementById('loginPage').classList.add('hidden');

  document.getElementById(pageName + 'Page').classList.remove('hidden');
}

// When login is clicked, go to home page
function goToHome() {
  window.location.href = 'result.html';
}