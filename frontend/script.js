let sessionId = null;
const messages = document.getElementById('messages');
const options = document.getElementById('options');
const progress = document.getElementById('progress');
const trace = document.getElementById('trace');
const profile = document.getElementById('profile');

function addBubble(text, who='bot') {
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
  (items || []).forEach(t => {
    const li = document.createElement('li');
    li.textContent = `${t.step}: ${t.status}`;
    trace.appendChild(li);
  });
}
function renderProfile(p) {
  if (!p) { profile.textContent = 'No profile yet.'; return; }
  const active = p.active_domains && p.active_domains.length ? p.active_domains.join(', ') : 'none';
  profile.innerHTML = `<strong>Status:</strong> ${p.diagnostic_status}<br><strong>Active domains:</strong> ${active}<br><strong>Boundary:</strong> ${p.clinical_boundary}`;
}
async function startSession() {
  const res = await fetch('/session/start', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ user_name: 'Demo User' }) });
  const data = await res.json();
  sessionId = data.session_id;
  messages.innerHTML = '';
  addBubble(data.message);
  addBubble(data.question.text);
  progress.textContent = data.progress;
  renderOptions(data.answer_options);
}
async function sendMessage(text) {
  if (!sessionId) return startSession();
  addBubble(text, 'user');
  const res = await fetch('/chat/message', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ session_id: sessionId, message: text }) });
  const data = await res.json();
  addBubble(data.message);
  if (data.question) addBubble(data.question.text);
  progress.textContent = data.progress || (data.session_complete ? 'Complete' : data.response_type);
  renderOptions(data.answer_options);
  renderTrace(data.decision_trace);
  renderProfile(data.dsm5_profile);
}
document.getElementById('startBtn').onclick = startSession;
document.getElementById('sendBtn').onclick = () => sendMessage(document.getElementById('messageInput').value);
