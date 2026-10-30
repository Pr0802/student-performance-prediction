/**
 * ==============================================================================
 * Student Performance Level Prediction - Client Logic
 * BCA College Project
 * Handles page navigation, form interactions, live calculation & API prediction
 * ==============================================================================
 */

// Global State
let currentTab = 'home';
let isBackendAvailable = true;

// Predefined Demo Samples for easy BCA Viva presentation
const SAMPLES = {
  high: {
    gender: 'female',
    parental_education: "bachelor's degree",
    lunch: 'standard',
    test_prep: 'completed',
    math: 85,
    reading: 88,
    writing: 91
  },
  medium: {
    gender: 'male',
    parental_education: 'some college',
    lunch: 'standard',
    test_prep: 'none',
    math: 64,
    reading: 68,
    writing: 63
  },
  low: {
    gender: 'female',
    parental_education: 'some high school',
    lunch: 'free/reduced',
    test_prep: 'none',
    math: 38,
    reading: 44,
    writing: 42
  }
};

// ==============================================================================
// 1. Navigation Controller (Single Page Architecture)
// ==============================================================================
function navigateTo(pageId) {
  currentTab = pageId;

  // Hide all sections
  document.querySelectorAll('.page-section').forEach(sec => {
    sec.classList.remove('active');
  });

  // Remove active from nav buttons
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.remove('active');
  });

  // Activate chosen page
  const targetPage = document.getElementById(`page-${pageId}`);
  if (targetPage) {
    targetPage.classList.add('active');
  }

  // Activate chosen button
  const targetBtn = document.getElementById(`nav-${pageId}`);
  if (targetBtn) {
    targetBtn.classList.add('active');
  }

  // Show "Result" tab button only when on Result page
  const resultNavBtn = document.getElementById('nav-result');
  if (resultNavBtn) {
    resultNavBtn.style.display = (pageId === 'result') ? 'inline-block' : 'none';
  }

  // Smooth scroll to top of page
  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Update hash without jumping
  history.replaceState(null, null, `#${pageId}`);
}

// ==============================================================================
// 2. Preset Fill & Live Calculations
// ==============================================================================
function fillPreset(type) {
  const data = SAMPLES[type];
  if (!data) return;

  document.getElementById('gender').value = data.gender;
  document.getElementById('parental_education').value = data.parental_education;
  document.getElementById('lunch').value = data.lunch;
  document.getElementById('test_prep').value = data.test_prep;
  document.getElementById('math_score').value = data.math;
  document.getElementById('reading_score').value = data.reading;
  document.getElementById('writing_score').value = data.writing;

  updateLiveAverage();
}

function resetForm() {
  document.getElementById('gender').value = 'male';
  document.getElementById('parental_education').value = 'some college';
  document.getElementById('lunch').value = 'standard';
  document.getElementById('test_prep').value = 'none';
  document.getElementById('math_score').value = '';
  document.getElementById('reading_score').value = '';
  document.getElementById('writing_score').value = '';

  updateLiveAverage();
}

function updateLiveAverage() {
  const m = parseFloat(document.getElementById('math_score').value) || 0;
  const r = parseFloat(document.getElementById('reading_score').value) || 0;
  const w = parseFloat(document.getElementById('writing_score').value) || 0;

  const avg = ((m + r + w) / 3).toFixed(1);
  const display = document.getElementById('live-avg-display');
  const badge = document.getElementById('live-category-badge');

  if (display) display.textContent = `${avg}%`;

  if (badge) {
    badge.className = 'badge-mini';
    if (avg >= 75) {
      badge.textContent = 'Likely High (≥75%)';
      badge.classList.add('green-pill');
    } else if (avg >= 50) {
      badge.textContent = 'Likely Medium (50–74%)';
      badge.classList.add('yellow-pill');
    } else {
      badge.textContent = 'Likely Low (<50%)';
      badge.classList.add('red-pill');
    }
  }
}

function updateModeUI() {
  const selectedMode = document.querySelector('input[name="prediction_mode"]:checked')?.value || 'ml';
  const mlCard = document.getElementById('mode-card-ml');
  const ruleCard = document.getElementById('mode-card-rule');

  if (selectedMode === 'ml') {
    mlCard?.classList.add('active');
    ruleCard?.classList.remove('active');
  } else {
    ruleCard?.classList.add('active');
    mlCard?.classList.remove('active');
  }
}

// ==============================================================================
// 3. Fallback Client-Side Prediction (In case server is offline)
// ==============================================================================
function clientSideRuleBased(m, r, w, gender, parent_edu, lunch, prep) {
  const avg = parseFloat(((m + r + w) / 3).toFixed(2));
  let level = 'MEDIUM';
  let message = 'Good academic performance. Consistent practice and revision will help achieve excellence.';
  let color = 'yellow';

  if (avg >= 75) {
    level = 'HIGH';
    message = 'Excellent academic performance! Keep it up.';
    color = 'green';
  } else if (avg < 50) {
    level = 'LOW';
    message = 'Needs academic improvement. Additional guidance and study hours recommended.';
    color = 'red';
  }

  return {
    status: 'success',
    average_score: avg,
    performance_level: level,
    message: message,
    color: color,
    model_used: 'Rule-Based Prototype (Client Offline Fallback)',
    is_ml_prediction: false,
    student_data: {
      gender: gender,
      parental_education: parent_edu,
      lunch: lunch,
      test_prep: prep,
      math_score: m,
      reading_score: r,
      writing_score: w
    }
  };
}

// ==============================================================================
// 4. Form Submit Handler (Connects to Flask Backend)
// ==============================================================================
async function handlePrediction(event) {
  event.preventDefault();

  const submitBtn = document.getElementById('predict-submit-btn');
  const btnText = document.getElementById('btn-text');

  // Collect form values
  const gender = document.getElementById('gender').value;
  const parent_edu = document.getElementById('parental_education').value;
  const lunch = document.getElementById('lunch').value;
  const test_prep = document.getElementById('test_prep').value;

  const math = parseFloat(document.getElementById('math_score').value);
  const reading = parseFloat(document.getElementById('reading_score').value);
  const writing = parseFloat(document.getElementById('writing_score').value);

  // Validate values
  if (isNaN(math) || isNaN(reading) || isNaN(writing)) {
    alert('Please enter valid numeric scores for all three subjects (0 to 100).');
    return;
  }

  if (math < 0 || math > 100 || reading < 0 || reading > 100 || writing < 0 || writing > 100) {
    alert('Subject marks must be between 0 and 100.');
    return;
  }

  const selectedMode = document.querySelector('input[name="prediction_mode"]:checked')?.value || 'ml';

  // Loading state
  submitBtn.disabled = true;
  btnText.textContent = 'Analyzing Student Data...';

  const payload = {
    gender: gender,
    parental_education: parent_edu,
    lunch: lunch,
    test_prep: test_prep,
    math_score: math,
    reading_score: reading,
    writing_score: writing,
    mode: selectedMode
  };

  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    const data = await response.json();
    renderResult(data);
  } catch (error) {
    console.warn('Backend request failed or offline. Switching to client-side prototype calculation:', error);
    // Instant seamless fallback to rule-based prototype
    const fallbackData = clientSideRuleBased(math, reading, writing, gender, parent_edu, lunch, test_prep);
    renderResult(fallbackData);
  } finally {
    submitBtn.disabled = false;
    btnText.textContent = 'Predict Performance';
  }
}

// ==============================================================================
// 5. Render Prediction Result Page
// ==============================================================================
function renderResult(data) {
  const mainCard = document.getElementById('result-main-card');
  const levelBanner = document.getElementById('result-level-banner');
  const avgScoreEl = document.getElementById('res-average-score');
  const levelEl = document.getElementById('res-performance-level');
  const messageEl = document.getElementById('res-message-text');
  const engineEl = document.getElementById('res-engine-name');
  const engineTag = document.getElementById('result-engine-tag');

  const mathVal = data.student_data.math_score;
  const readingVal = data.student_data.reading_score;
  const writingVal = data.student_data.writing_score;

  // Set values
  avgScoreEl.textContent = `${data.average_score}%`;
  levelEl.textContent = data.performance_level;
  messageEl.textContent = `“${data.message}”`;
  engineEl.textContent = data.model_used;

  // Timestamp
  const now = new Date();
  document.getElementById('res-timestamp').textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // Reset classes
  mainCard.className = 'result-card';
  levelBanner.className = 'result-level-banner';

  // Apply Category Color Themes:
  // Red for Low Performance
  // Yellow for Medium Performance
  // Green for High Performance
  const color = data.color.toLowerCase();
  if (color === 'green' || data.performance_level === 'HIGH') {
    mainCard.classList.add('theme-green');
    levelBanner.classList.add('green-mode');
    document.getElementById('res-message-icon').textContent = '🌟';
  } else if (color === 'yellow' || data.performance_level === 'MEDIUM') {
    mainCard.classList.add('theme-yellow');
    levelBanner.classList.add('yellow-mode');
    document.getElementById('res-message-icon').textContent = '📈';
  } else {
    mainCard.classList.add('theme-red');
    levelBanner.classList.add('red-mode');
    document.getElementById('res-message-icon').textContent = '⚠️';
  }

  // Distinction between ML and Rule-based
  if (data.is_ml_prediction) {
    engineTag.style.background = '#E0F2FE';
    engineTag.style.color = '#0369A1';
  } else {
    engineTag.style.background = '#FEF3C7';
    engineTag.style.color = '#92400E';
  }

  // Subject Marks & Bars
  document.getElementById('res-math-score').textContent = `${mathVal}/100`;
  document.getElementById('res-reading-score').textContent = `${readingVal}/100`;
  document.getElementById('res-writing-score').textContent = `${writingVal}/100`;

  document.getElementById('res-math-bar').style.width = `${mathVal}%`;
  document.getElementById('res-reading-bar').style.width = `${readingVal}%`;
  document.getElementById('res-writing-bar').style.width = `${writingVal}%`;

  // Student Profile
  document.getElementById('res-gender').textContent = data.student_data.gender;
  document.getElementById('res-parent-edu').textContent = data.student_data.parental_education;
  document.getElementById('res-lunch').textContent = data.student_data.lunch;
  document.getElementById('res-test-prep').textContent = data.student_data.test_prep;

  // Navigate to Result Page
  navigateTo('result');
}

// ==============================================================================
// 6. Check ML Backend Health on Startup
// ==============================================================================
async function checkBackendStatus() {
  const statusPill = document.getElementById('model-status-indicator');
  const statusText = document.getElementById('model-status-text');

  try {
    const res = await fetch('/api/status');
    if (res.ok) {
      const info = await res.json();
      if (info.ml_available) {
        statusText.textContent = `ML Active (${info.accuracy}% Acc)`;
      } else {
        statusText.textContent = 'Rule-Based Mode';
        statusPill.style.background = '#FEF3C7';
        statusPill.style.color = '#92400E';
        statusPill.style.borderColor = '#FCD34D';
        document.querySelector('.status-dot').style.background = '#F59E0B';
      }
    }
  } catch (e) {
    // Running statically
    if (statusText) statusText.textContent = 'Standalone Mode';
  }
}

// ==============================================================================
// 7. Initialization on DOM Load
// ==============================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Check hash for direct bookmark
  const hash = window.location.hash.replace('#', '');
  if (['home', 'predict', 'result', 'about'].includes(hash)) {
    navigateTo(hash);
  } else {
    navigateTo('home');
  }

  // Setup input change listeners for live average calculator
  ['math_score', 'reading_score', 'writing_score'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', updateLiveAverage);
    }
  });

  updateModeUI();
  updateLiveAverage();
  checkBackendStatus();
});
