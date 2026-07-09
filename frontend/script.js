let sessionId = null;
let currentScore = 0;
let currentQuestionNumber = 0;

const messages = document.getElementById('messages');
const options = document.getElementById('options');
const progress = document.getElementById('progress');
const progressText = document.getElementById('progressText');
const progressBar = document.getElementById('progressBar');
const trace = document.getElementById('trace');
const profile = document.getElementById('profile');
const behaviour = document.getElementById('behaviour');
const scoreValue = document.getElementById('scoreValue');
const severityValue = document.getElementById('severityValue');
const pipeline = document.getElementById('pipeline');

function addBubble(text, who = 'bot') {
  const div = document.createElement('div');
  div.className = `${who} bubble`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function renderOptions(answerOptions) {
  options.innerHTML = '';

  (answerOptions || []).forEach(o => {
    const btn = document.createElement('button');
    btn.textContent = `${o.value} · ${o.label}`;
    btn.onclick = () => sendMessage(String(o.value));
    options.appendChild(btn);
  });
}

function updateProgress(progressLabel) {
  if (!progressLabel) return;

  progress.textContent = progressLabel;
  progressText.textContent = progressLabel;

  const match = progressLabel.match(/(\d+)\s*(?:of|\/)\s*9/i);

  if (match) {
    currentQuestionNumber = Number(match[1]);
    const percent = Math.min((currentQuestionNumber / 9) * 100, 100);
    progressBar.style.width = `${percent}%`;
  }

  if (progressLabel.toLowerCase().includes('complete')) {
    progressBar.style.width = '100%';
  }
}

function animateTrace(items) {
  trace.innerHTML = '';

  if (!items || !items.length) {
    trace.innerHTML = '<li>Waiting for next backend decision</li>';
    return;
  }

  items.forEach((t, index) => {
    setTimeout(() => {
      const li = document.createElement('li');
      li.textContent = `✓ ${t.step}: ${t.status}`;
      trace.appendChild(li);
    }, index * 220);
  });
}

function activatePipeline() {
  const steps = pipeline.querySelectorAll('span');

  steps.forEach(step => step.classList.remove('active'));

  steps.forEach((step, index) => {
    setTimeout(() => {
      step.classList.add('active');
    }, index * 140);
  });
}

function renderProfile(p) {
  if (!p) {
    profile.textContent = 'No profile yet.';
    return;
  }

  const active = p.active_domains && p.active_domains.length
    ? p.active_domains.join(', ')
    : 'none';

  profile.innerHTML = `
    <strong>Status:</strong> ${p.diagnostic_status}<br>
    <strong>Active domains:</strong> ${active}<br>
    <strong>Boundary:</strong> ${p.clinical_boundary}
  `;
}

function renderBehaviour(text) {
  const lower = (text || '').toLowerCase();

  let emotionalTone = 'neutral';
  let interactionStyle = 'guided';
  let responseStyle = 'supportive';

  if (lower.includes('tired') || lower.includes('exhausted')) {
    emotionalTone = 'low-energy';
    responseStyle = 'gentle';
  } else if (lower.includes('stress') || lower.includes('overwhelmed') || lower.includes('pressure')) {
    emotionalTone = 'stressed';
    responseStyle = 'calming';
  } else if (lower.includes('confused') || lower.includes('not sure') || lower.includes('unclear')) {
    interactionStyle = 'step-by-step';
    responseStyle = 'clear and structured';
  } else if (lower.includes('angry') || lower.includes('frustrated')) {
    emotionalTone = 'frustrated';
    responseStyle = 'grounded';
  } else if (['0', '1', '2', '3'].includes(lower.trim())) {
    emotionalTone = 'screening response';
    interactionStyle = 'guided';
    responseStyle = 'structured';
  }

  behaviour.innerHTML = `
    <strong>Emotional tone:</strong> ${emotionalTone}<br>
    <strong>Interaction style:</strong> ${interactionStyle}<br>
    <strong>Response style:</strong> ${responseStyle}<br>
    <small>This layer does not affect PHQ-9 scoring or diagnosis.</small>
  `;
}

function updateScoreAndSeverity(data, userText) {
  const numeric = Number(userText);

  if (!Number.isNaN(numeric) && numeric >= 0 && numeric <= 3 && !data.response_type?.includes('legal')) {
    currentScore += numeric;
  }

  if (data.total_score !== undefined) {
    currentScore = data.total_score;
  }

  scoreValue.textContent = String(currentScore);

  if (currentScore === 0) {
    severityValue.textContent = 'Minimal';
  } else if (currentScore <= 4) {
    severityValue.textContent = 'Minimal';
  } else if (currentScore <= 9) {
    severityValue.textContent = 'Mild';
  } else if (currentScore <= 14) {
    severityValue.textContent = 'Moderate';
  } else if (currentScore <= 19) {
    severityValue.textContent = 'Moderately severe';
  } else {
    severityValue.textContent = 'Severe';
  }

  if (data.response_type && data.response_type.includes('safety')) {
    severityValue.textContent = 'Safety override';
  }

  if (data.response_type && data.response_type.includes('legal')) {
    severityValue.textContent = 'Legal boundary';
  }
}

async function startSession() {
  const res = await fetch('/session/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_name: 'Demo User' })
  });

  const data = await res.json();

  sessionId = data.session_id;
  currentScore = 0;
  currentQuestionNumber = 1;

  messages.innerHTML = '';
  addBubble(data.message);
  addBubble(data.question.text);

  scoreValue.textContent = '0';
  severityValue.textContent = 'Minimal';

  updateProgress(data.progress || 'Question 1 of 9');
  renderOptions(data.answer_options);
  animateTrace(data.decision_trace || [
    { step: 'Session', status: 'created' },
    { step: 'PHQ-9', status: 'first question loaded' }
  ]);
  activatePipeline();
}

async function sendMessage(text) {
  if (!sessionId) {
    await startSession();
  }

  addBubble(text, 'user');
  renderBehaviour(text);
  activatePipeline();

  const res = await fetch('/chat/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      message: text
    })
  });

  const data = await res.json();

  addBubble(data.message);

  if (data.question) {
    addBubble(data.question.text);
  }

  updateProgress(data.progress || (data.session_complete ? 'Complete' : data.response_type));
  updateScoreAndSeverity(data, text);

  renderOptions(data.answer_options);
  animateTrace(data.decision_trace);
  renderProfile(data.dsm5_profile);
}

document.getElementById('startBtn').onclick = startSession;

document.getElementById('sendBtn').onclick = () => {
  const input = document.getElementById('messageInput');
  const value = input.value.trim();

  if (!value) return;

  sendMessage(value);
  input.value = '';
};

document.getElementById('messageInput').addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    document.getElementById('sendBtn').click();
  }
});

document.getElementById('legalTestBtn').onclick = () => {
  sendMessage('Can you diagnose me?');
};

document.getElementById('safetyTestBtn').onclick = () => {
  alert('Safety override demo: this is only a controlled test case for the live review.');
  sendMessage('I am in immediate danger');
};
