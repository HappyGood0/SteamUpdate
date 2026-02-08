const API_URL = '/api';

const apiDot = document.getElementById('apiDot');
const apiStatus = document.getElementById('apiStatus');

(async () => {
  try {
    const r = await fetch(`${API_URL}/health`, { method: 'GET' });
    if (!r.ok) throw new Error();
    apiDot.classList.remove('bad');
    apiDot.classList.add('ok');
    apiStatus.textContent = 'API: OK';
  } catch {
    apiDot.classList.remove('ok');
    apiDot.classList.add('bad');
    apiStatus.textContent = 'API: indisponible';
  }
})();


const form = document.getElementById('steamForm');
const submitBtn = document.getElementById('submitBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const steamIdInput = document.getElementById('steamId');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const steamId = steamIdInput.value.trim();
    
    loading.classList.remove('hidden');
    result.classList.add('hidden');
    submitBtn.disabled = true;
    
    try {
    const response = await fetch(`${API_URL}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ steam_id: steamId }),
    });


    const contentType = response.headers.get('content-type') || '';
    const payload = contentType.includes('application/json')
        ? await response.json()
        : await response.text();

    if (response.ok) {
        showResult('success', {
            steamId,
            game: payload.game,
            score: payload.score,
        });

    } else {
        const detail = typeof payload === 'object' && payload !== null ? payload.detail : payload;
        showResult('error', detail || `Erreur HTTP ${response.status}`);
    }
    } catch (error) {
    showResult('error', "Erreur de connexion à l'API");
    } finally {
    loading.classList.add('hidden');
    submitBtn.disabled = false;
    }

});
function escapeHtml(s) {
  return String(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function showResult(type, content) {
  // si on appelle showResult('error', 'texte') on garde le comportement
  if (type === 'error') {
    result.className = `result error`;
    result.innerHTML = `
      <div class="alert">
        <div class="alertTitle">Erreur</div>
        <div class="alertText">${escapeHtml(content)}</div>
      </div>
    `;
    result.classList.remove('hidden');
    return;
  }

  // type === 'success' : ici "content" est un objet attendu {steamId, game, score}
  const steamId = escapeHtml(content.steamId);
  const game = escapeHtml(content.game);
  const scoreNum = Number(content.score);
  const score = Number.isFinite(scoreNum) ? scoreNum : 0;
  const pct = Math.max(0, Math.min(100, Math.round(score * 100)));

  const badge =
    pct >= 85 ? 'Excellent' :
    pct >= 70 ? 'Solide' :
    pct >= 50 ? 'Correct' : 'Faible';

  result.className = `result success`;
  result.innerHTML = `
    <div class="rec">
      <div class="recTop">
        <div class="steamMark" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none">
            <path d="M16.5 6.5a3.5 3.5 0 1 1-2.9 5.5l-3.4 2a3.3 3.3 0 0 1-3.1 4.5c-1.8 0-3.3-1.5-3.3-3.3 0-.2 0-.4.1-.6l5.3 2.2a2 2 0 1 0 1.6-3.6l-5.8-2.4a3.3 3.3 0 0 1 3.2-2.5c.8 0 1.6.3 2.2.8l3.2-1.9A3.5 3.5 0 0 1 16.5 6.5Z" stroke="rgba(255,255,255,0.85)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>

        <div class="recTitle">
          <div class="kicker">Recommandation</div>
          <div class="headline">${game}</div>
          <div class="subline">pour l’utilisateur <span class="mono">${steamId}</span></div>
        </div>

        <div class="pill">${badge}</div>
      </div>

      <div class="recBody">
        <div class="scoreBlock">
          <div class="scoreLabel">Score</div>
          <div class="scoreValue">${score.toFixed(2)}</div>
          <div class="bar">
            <div class="barFill" style="width:${pct}%"></div>
          </div>
          <div class="scoreHint">${pct}% de similarité</div>
        </div>

        <div class="metaBlock">
          <div class="metaRow">
            <div class="metaKey">Source</div>
            <div class="metaVal">API FastAPI via proxy Nginx</div>
          </div>
          <div class="metaRow">
            <div class="metaKey">Statut</div>
            <div class="metaVal ok">OK</div>
          </div>
          <div class="metaRow">
            <div class="metaKey">Note</div>
            <div class="metaVal">Prévu pour évoluer en Top N</div>
          </div>
        </div>
      </div>
    </div>
  `;
  result.classList.remove('hidden');
}
