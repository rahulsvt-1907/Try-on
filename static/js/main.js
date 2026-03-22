// Home page JS: filtering, search, and try-on navigation

let currentGender = 'All';
let currentCategory = 'All';

function setGenderFilter(gender) {
  currentGender = gender;
  document.querySelectorAll('.gender-btn').forEach(btn => {
    const isActive = btn.dataset.gender === gender;
    btn.className = btn.className
      .replace(/bg-purple-600 text-white border-purple-600/g, '')
      .replace(/bg-white text-gray-600 border-gray-200/g, '');
    if (isActive) {
      btn.classList.add('bg-purple-600', 'text-white', 'border-purple-600');
      btn.classList.remove('bg-white', 'text-gray-600', 'border-gray-200');
    } else {
      btn.classList.add('bg-white', 'text-gray-600', 'border-gray-200');
      btn.classList.remove('bg-purple-600', 'text-white', 'border-purple-600');
    }
  });
  filterPins();
}

function setCategoryFilter(category) {
  currentCategory = category;
  document.querySelectorAll('.category-btn').forEach(btn => {
    const isActive = btn.dataset.category === category;
    if (isActive) {
      btn.classList.add('bg-purple-600', 'text-white', 'border-purple-600');
      btn.classList.remove('bg-white', 'text-gray-600', 'border-gray-200');
    } else {
      btn.classList.remove('bg-purple-600', 'text-white', 'border-purple-600');
      btn.classList.add('bg-white', 'text-gray-600', 'border-gray-200');
    }
  });
  filterPins();
}

function filterPins() {
  const query = (document.getElementById('search-input').value || '').toLowerCase().trim();
  const cards = document.querySelectorAll('.pin-card');
  let visible = 0;

  cards.forEach(card => {
    const gender = card.dataset.gender || '';
    const category = card.dataset.category || '';
    const title = (card.dataset.title || '').toLowerCase();
    const alt = (card.dataset.alt || '').toLowerCase();

    const genderMatch = currentGender === 'All' || gender === currentGender || gender === '';
    const categoryMatch = currentCategory === 'All' || category === currentCategory;
    const searchMatch = !query || title.includes(query) || alt.includes(query);

    if (genderMatch && categoryMatch && searchMatch) {
      card.style.display = '';
      visible++;
    } else {
      card.style.display = 'none';
    }
  });

  const countEl = document.getElementById('results-count');
  if (countEl) countEl.textContent = `Showing ${visible} item${visible !== 1 ? 's' : ''}`;

  const noResults = document.getElementById('no-results');
  if (noResults) {
    noResults.classList.toggle('hidden', visible > 0);
  }
}

function tryOnPin(imageUrl) {
  window.location.href = '/tryon?q=' + encodeURIComponent(imageUrl);
}

// Initialise count on load
document.addEventListener('DOMContentLoaded', function () {
  filterPins();
});
