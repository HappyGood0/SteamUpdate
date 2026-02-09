const IS_GH_PAGES = window.location.hostname.endsWith("github.io");
const RENDER_ORIGIN = "https://steamupdate.onrender.com";
const API_ORIGIN = IS_GH_PAGES ? RENDER_ORIGIN : "";
const API_URL = `${API_ORIGIN}/api`;


const apiDot = document.getElementById("apiDot");
const apiStatus = document.getElementById("apiStatus");

(async () => {
  try {
    const r = await fetch(`${API_URL}/health`, { method: "GET" });
    if (!r.ok) throw new Error();
    apiDot.classList.remove("bad");
    apiDot.classList.add("ok");
    apiStatus.textContent = "API: OK";
  } catch {
    apiDot.classList.remove("ok");
    apiDot.classList.add("bad");
    apiStatus.textContent = "API: indisponible";
  }
})();

const form = document.getElementById("steamForm");
const submitBtn = document.getElementById("submitBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const steamIdInput = document.getElementById("steamId");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const steamId = steamIdInput.value.trim();
    
    loading.classList.remove("hidden");
    result.classList.add("hidden");
    submitBtn.disabled = true;
    
    try {
    const response = await fetch(`${API_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ steam_id: steamId }),
    });

    const contentType = response.headers.get("content-type") || "";
    const payload = contentType.includes("application/json")
        ? await response.json()
        : await response.text();

    if (response.ok) {
        // Nouveau format: { steam_id, recommendations: [...] }
        if (payload && Array.isArray(payload.recommendations) && payload.recommendations.length > 0) {
            // reset le container pour empiler les résultats
        result.innerHTML = "";
        result.classList.add("hidden");

        payload.recommendations.forEach((rec) => {
          showResult("success", {
            steamId,
            game: rec.nom ?? rec.name ?? rec.game ?? "N/A",
            image: rec.img,
            link: rec.lien,
            score: rec.score ?? 0.95,
          });
        });

        } else {
            // Ancien format: { steam_id, game, score }
            showResult("success", {
                steamId,
                game: payload.game ?? "N/A",
                score: payload.score ?? 0,
            });
        }
    } else {
        const detail = typeof payload === "object" && payload !== null ? payload.detail : payload;
        showResult("error", detail || `Erreur HTTP ${response.status}`);
    }
    } catch {
    showResult("error", "Erreur de connexion à l'API");
    } finally {
    loading.classList.add("hidden");
    submitBtn.disabled = false;
  }
});

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll("'", "&#039;");
}

function showResult(type, content) {
  // si on appelle showResult('error', 'texte') on garde le comportement
  if (type === "error") {
    result.className = "result error";
    result.innerHTML = `
      <div class="alert">
        <div class="alertTitle">Erreur</div>
        <div class="alertText">${escapeHtml(content)}</div>
      </div>
    `;
    result.classList.remove("hidden");
    return;
  }

  // type === 'success' : ici "content" est un objet attendu {steamId, game, score}
  const steamId = escapeHtml(content.steamId);
  const game = escapeHtml(content.game);
  const scoreNum = Number(content.score);
  const score = Number.isFinite(scoreNum) ? scoreNum : 0;
  const image = content.image ? escapeHtml(content.image) : null;
  const link = content.link ? escapeHtml(content.link) : null;
  const pct = Math.max(0, Math.min(100, Math.round(score * 100)));

  const badge =
    pct >= 85 ? "Excellent" :
    pct >= 70 ? "Solide" :
    pct >= 50 ? "Correct" : "Faible";

  result.className = "result success";
  result.insertAdjacentHTML("beforeend", `
  <div class="rec">
    <div class="recTop recTopWithImage">

      ${
        image
          ? `<div class="recImage">
               <img src="${image}" alt="${game}">
             </div>`
          : ""
      }

      <div class="recTitle">
        <div class="kicker">Recommandation</div>

        ${
          link
            ? `<a class="headline" href="${link}" target="_blank" rel="noopener">${game}</a>`
            : `<div class="headline">${game}</div>`
        }

        <div class="subline">
          pour l’utilisateur <span class="mono">${steamId}</span>
        </div>
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
    </div>
  </div>
`);


  result.classList.remove("hidden");
}
