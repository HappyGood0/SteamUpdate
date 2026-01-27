const API_URL = 'http://localhost:8000/api';

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
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ steam_id: steamId })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult('success', `Utilisateur: ${steamId}<br>Jeu: ${data.game}<br>Score: ${data.score}`);
        } else {
            showResult('error', data.detail || 'Erreur');
        }
    } catch (error) {
        showResult('error', 'Erreur de connexion à l\'API');
    } finally {
        loading.classList.add('hidden');
        submitBtn.disabled = false;
    }
});

function showResult(type, content) {
    result.className = type;
    result.innerHTML = content;
    result.classList.remove('hidden');
}