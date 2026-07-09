let sessionId = null;

const messages = document.getElementById('messages');
const options = document.getElementById('options');
const progress = document.getElementById('progress');
const trace = document.getElementById('trace');
const profile = document.getElementById('profile');
const behaviour = document.getElementById('behaviour');

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

function renderTrace(items) {
  trace.innerHTML = '';

  if (!items || !items.length) {
    trace.innerHTML = '<li>Waiting for next backend decision</li>';
    return;
  }

  items.forEach(t => {
    const li = document.createElement('li');
    li.textContent = `✓ ${t.step}: ${t.status}`;
    trace.appendChild(li);
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
  } else if (lower.includes('stress') || lower.includes('overwhelmed')) {
    emotionalTone = 'stressed';
    responseStyle = 'calming';
  } else if (lower.includes('confused') || lower.includes('not sure')) {
    interactionStyle = 'step-by-step';
    responseStyle = 'clear and structured';
  } else if (lower.includes('angry') || lower.includes('frustrated')) {
    emotionalTone = 'frustrated';
    responseStyle = 'grounded';
  }

  behaviour.innerHTML = `
    <strong>Emotional tone:</strong> ${emotionalTone}<br>
    <strong>Interaction style:</strong> ${interactionStyle}<br>
    <strong>Response style:</strong> ${responseStyle}<br>
    <small>This layer does not affect PHQ-9 scoring or diagnosis.</small>
  `;
}

async function startSession() {
  const res = await fetch('/session/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_name: 'Demo User' })
  });

  const data = await res.json();
  sessionId = data.session_id;

  messages.innerHTML = '';
  addBubble(data.message);
  addBubble(data.question.text);

  progress.textContent = data.progress;
  renderOptions(data.answer_options);
  renderTrace(data.decision_trace);
}

async function sendMessage(text) {
  if (!sessionId) {
    await startSession();
  }

  addBubble(text, 'user');
  renderBehaviour(text);

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

  progress.textContent = data.progress || (data.session_complete ? 'Complete' : data.response_type);

  renderOptions(data.answer_options);
  renderTrace(data.decision_trace);
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
