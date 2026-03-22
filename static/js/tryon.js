// Try-on page JS: handles image inputs, API call, and result display

let avatarFile = null;
let clothingFile = null;
let avatarMode = 'both';
let clothingMode = 'both';
let etaInterval = null;

// ---- Mode switching ----

function setAvatarMode(mode) {
  avatarMode = mode;
  document.querySelectorAll('[data-avatar-mode]').forEach(btn => {
    const active = btn.dataset.avatarMode === mode;
    if (active) {
      btn.classList.add('bg-purple-600', 'text-white', 'border-purple-600');
      btn.classList.remove('bg-white', 'text-gray-500', 'border-gray-200');
    } else {
      btn.classList.remove('bg-purple-600', 'text-white', 'border-purple-600');
      btn.classList.add('bg-white', 'text-gray-500', 'border-gray-200');
    }
  });
  const imgSec = document.getElementById('avatar-image-section');
  const promptSec = document.getElementById('avatar-prompt-section');
  imgSec.style.display = mode === 'prompt' ? 'none' : '';
  promptSec.style.display = mode === 'image' ? 'none' : '';
  updateGenerateButton();
}

function setClothingMode(mode) {
  clothingMode = mode;
  document.querySelectorAll('[data-clothing-mode]').forEach(btn => {
    const active = btn.dataset.clothingMode === mode;
    if (active) {
      btn.classList.add('bg-teal-600', 'text-white', 'border-teal-600');
      btn.classList.remove('bg-white', 'text-gray-500', 'border-gray-200');
    } else {
      btn.classList.remove('bg-teal-600', 'text-white', 'border-teal-600');
      btn.classList.add('bg-white', 'text-gray-500', 'border-gray-200');
    }
  });
  const imgSec = document.getElementById('clothing-image-section');
  const promptSec = document.getElementById('clothing-prompt-section');
  imgSec.style.display = mode === 'prompt' ? 'none' : '';
  promptSec.style.display = mode === 'image' ? 'none' : '';
  updateGenerateButton();
}

// ---- Image handling ----

function handleAvatarImage(event) {
  const file = event.target.files[0];
  if (!file) return;
  if (!validateImage(file)) return;
  avatarFile = file;
  const url = URL.createObjectURL(file);
  document.getElementById('avatar-preview').src = url;
  document.getElementById('avatar-preview-wrap').classList.remove('hidden');
  document.getElementById('avatar-upload-area').classList.add('hidden');
  updateGenerateButton();
}

function clearAvatarImage() {
  avatarFile = null;
  document.getElementById('avatar-input').value = '';
  document.getElementById('avatar-preview-wrap').classList.add('hidden');
  document.getElementById('avatar-upload-area').classList.remove('hidden');
  updateGenerateButton();
}

function handleClothingImage(event) {
  const file = event.target.files[0];
  if (!file) return;
  if (!validateImage(file)) return;
  clothingFile = file;
  const url = URL.createObjectURL(file);
  document.getElementById('clothing-preview').src = url;
  document.getElementById('clothing-preview-wrap').classList.remove('hidden');
  document.getElementById('clothing-upload-area').classList.add('hidden');
  updateGenerateButton();
}

function clearClothingImage() {
  clothingFile = null;
  document.getElementById('clothing-input').value = '';
  document.getElementById('clothing-preview-wrap').classList.add('hidden');
  document.getElementById('clothing-upload-area').classList.remove('hidden');
  updateGenerateButton();
}

function validateImage(file) {
  const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!validTypes.includes(file.type)) {
    showError('Please upload a JPEG, PNG, or WebP image.');
    return false;
  }
  if (file.size > 4 * 1024 * 1024) {
    showError('Image size must be ≤4MB.');
    return false;
  }
  return true;
}

// ---- Button state ----

function updateGenerateButton() {
  const avatarPrompt = document.getElementById('avatar-prompt').value.trim();
  const clothingPrompt = document.getElementById('clothing-prompt').value.trim();
  const hasAvatar = avatarFile || avatarPrompt;
  const hasClothing = clothingFile || clothingPrompt;
  const btn = document.getElementById('try-on-btn');
  if (hasAvatar && hasClothing) {
    btn.disabled = false;
    btn.className = 'w-full py-3 rounded-xl text-lg font-semibold shadow-sm transition-all duration-200 bg-gradient-to-r from-teal-500 to-purple-500 text-white hover:from-teal-600 hover:to-purple-600 cursor-pointer';
  } else {
    btn.disabled = true;
    btn.className = 'w-full py-3 rounded-xl text-lg font-semibold shadow-sm transition-all duration-200 bg-gray-200 text-gray-400 cursor-not-allowed';
  }
}

// ---- Error display ----

function showError(msg) {
  const banner = document.getElementById('error-banner');
  document.getElementById('error-text').textContent = msg;
  banner.classList.remove('hidden');
}

function hideError() {
  document.getElementById('error-banner').classList.add('hidden');
}

// ---- ETA progress ----

function startEta() {
  const etaSequence = ['1/15 seconds', '15/20 seconds', '18/25 seconds', '20/30 seconds'];
  let index = 0;
  const btn = document.getElementById('try-on-btn');
  etaInterval = setInterval(() => {
    btn.textContent = 'Processing... ' + etaSequence[index];
    index = (index + 1) % etaSequence.length;
  }, 1000);
}

function stopEta() {
  if (etaInterval) {
    clearInterval(etaInterval);
    etaInterval = null;
  }
  document.getElementById('try-on-btn').textContent = 'Try On';
}

// ---- Main try-on call ----

async function handleTryOn() {
  hideError();
  document.getElementById('result-section').classList.add('hidden');

  const avatarPrompt = document.getElementById('avatar-prompt').value.trim();
  const clothingPrompt = document.getElementById('clothing-prompt').value.trim();

  if (!avatarFile && !avatarPrompt) {
    showError('Please provide an avatar image or prompt.');
    return;
  }
  if (!clothingFile && !clothingPrompt) {
    showError('Please provide a clothing image or prompt.');
    return;
  }

  const btn = document.getElementById('try-on-btn');
  btn.disabled = true;
  startEta();

  const formData = new FormData();
  if (avatarFile) formData.append('avatar_image', avatarFile);
  if (clothingFile) formData.append('clothing_image', clothingFile);
  if (avatarPrompt) formData.append('avatar_prompt', avatarPrompt);
  if (clothingPrompt) formData.append('clothing_prompt', clothingPrompt);

  const backgroundPrompt = document.getElementById('background-prompt').value.trim();
  if (backgroundPrompt) formData.append('background_prompt', backgroundPrompt);

  const avatarSex = document.getElementById('avatar-sex').value;
  if (avatarSex) formData.append('avatar_sex', avatarSex);

  const seed = document.getElementById('seed').value.trim();
  if (seed) formData.append('seed', seed);

  try {
    const response = await fetch('/api/try-on', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      let errorMsg = 'API request failed';
      try {
        const errData = await response.json();
        errorMsg = errData.error || errorMsg;
      } catch (e) {}
      showError(errorMsg);
      return;
    }

    const contentType = response.headers.get('Content-Type') || '';
    if (!contentType.startsWith('image/')) {
      showError('Unexpected response format from AI service.');
      return;
    }

    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);
    const resultImg = document.getElementById('result-image');
    resultImg.src = imageUrl;
    document.getElementById('download-btn').href = imageUrl;
    document.getElementById('result-section').classList.remove('hidden');
    document.getElementById('result-section').scrollIntoView({ behavior: 'smooth' });

  } catch (err) {
    showError(err.message || 'An unexpected error occurred.');
  } finally {
    stopEta();
    updateGenerateButton();
  }
}

// ---- Share ----

async function shareResult() {
  const resultImg = document.getElementById('result-image');
  if (!resultImg.src) return;
  try {
    if (navigator.share) {
      const blob = await fetch(resultImg.src).then(r => r.blob());
      const file = new File([blob], 'tryon-result.jpg', { type: blob.type });
      await navigator.share({ title: 'My Try-On Result', files: [file] });
    } else {
      await navigator.clipboard.writeText(window.location.href);
      alert('Page URL copied to clipboard!');
    }
  } catch (err) {
    // Share was cancelled or failed silently
  }
}

// ---- Init ----

document.addEventListener('DOMContentLoaded', function () {
  // Load clothing image from query param (clicked from catalog)
  const params = new URLSearchParams(window.location.search);
  const qUrl = params.get('q');
  if (qUrl) {
    loadClothingFromUrl(qUrl);
  }

  // Auto-populate avatar from saved profile
  try {
    const stored = localStorage.getItem('styleAIProfile');
    if (stored) {
      const profile = JSON.parse(stored);
      if (profile.image && profile.image.startsWith('data:image/')) {
        // Convert data URL to File
        fetch(profile.image)
          .then(r => r.blob())
          .then(blob => {
            const file = new File([blob], 'avatar.jpg', { type: blob.type });
            avatarFile = file;
            document.getElementById('avatar-preview').src = profile.image;
            document.getElementById('avatar-preview-wrap').classList.remove('hidden');
            document.getElementById('avatar-upload-area').classList.add('hidden');
            if (profile.sex) document.getElementById('avatar-sex').value = profile.sex.toLowerCase();
            updateGenerateButton();
          });
      }
    }
  } catch (e) {}

  // Update button state on prompt input
  document.getElementById('avatar-prompt').addEventListener('input', updateGenerateButton);
  document.getElementById('clothing-prompt').addEventListener('input', updateGenerateButton);
});

async function loadClothingFromUrl(url) {
  try {
    if (url.startsWith('data:image/')) {
      // Inline data URL
      const res = await fetch(url);
      const blob = await res.blob();
      clothingFile = new File([blob], 'clothing.jpg', { type: blob.type });
      document.getElementById('clothing-preview').src = url;
      document.getElementById('clothing-preview-wrap').classList.remove('hidden');
      document.getElementById('clothing-upload-area').classList.add('hidden');
    } else {
      // Proxy external image through backend
      const res = await fetch('/api/proxy-image?url=' + encodeURIComponent(url));
      if (!res.ok) throw new Error('Failed to fetch image');
      const blob = await res.blob();
      clothingFile = new File([blob], 'clothing.jpg', { type: blob.type });
      const objUrl = URL.createObjectURL(blob);
      document.getElementById('clothing-preview').src = objUrl;
      document.getElementById('clothing-preview-wrap').classList.remove('hidden');
      document.getElementById('clothing-upload-area').classList.add('hidden');
    }
    updateGenerateButton();
  } catch (err) {
    showError('Failed to load clothing image from URL.');
  }
}
