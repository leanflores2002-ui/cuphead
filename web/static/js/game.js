/* Minimal 2D canvas + fetch loop for the boss rush game. */

const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const hud = document.getElementById('hud');
const resultText = document.getElementById('result-text');
const profileStatus = document.getElementById('profile-status');

let activeName = null;
let polling = null;

function drawState(state) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // draw ground
  ctx.fillStyle = '#333';
  ctx.fillRect(0, 150, canvas.width, 2);

  // player (blue)
  if (state.player) {
    const p = state.player;
    ctx.fillStyle = '#6cf';
    ctx.fillRect(p.position[0] - 10, 140, 20, 20);
    // health bar
    ctx.fillStyle = '#f55';
    ctx.fillRect(10, 10, Math.max(0, p.health), 6);
  }

  // enemy (red)
  if (state.enemy) {
    const e = state.enemy;
    ctx.fillStyle = '#f66';
    ctx.fillRect(e.position[0] - 10, 120, 20, 20);
    ctx.fillStyle = '#6f6';
    ctx.fillRect(10, 24, Math.max(0, e.health), 6);
  }
}

async function api(path, method = 'GET', body) {
  const res = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json().catch(() => ({}));
}

async function poll() {
  try {
    const state = await api('/api/state');
    drawState(state);
    hud.textContent = `Frame: ${state.frame} | Player HP: ${state.player.health} | Enemy HP: ${state.enemy ? state.enemy.health : '-'} `;
    if (state.enemy && !state.enemy.alive) {
      resultText.textContent = `¡Victoria! Derrotaste a ${state.enemy.name}.`;
      clearInterval(polling);
    } else if (!state.player.alive) {
      resultText.textContent = 'Derrota. Vuelve a intentarlo.';
      clearInterval(polling);
    }
  } catch (e) {
    console.warn('poll error', e);
  }
}

document.getElementById('create-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  try {
    const profile = await api('/api/knight', 'POST', { name });
    activeName = profile.name;
    profileStatus.textContent = `Perfil activo: ${activeName}`;
  } catch (err) {
    profileStatus.textContent = 'Error creando perfil (nombre inválido o duplicado)';
  }
});

document.getElementById('start').addEventListener('click', async () => {
  if (!activeName) {
    profileStatus.textContent = 'Crea un perfil primero';
    return;
  }
  const boss = document.getElementById('boss').value;
  await api(`/api/start_boss/${boss}`, 'POST', { name: activeName });
  resultText.textContent = '';
  if (polling) clearInterval(polling);
  polling = setInterval(poll, 200);
});

document.querySelectorAll('#game .controls button').forEach((btn) => {
  btn.addEventListener('click', async () => {
    const action = btn.dataset.action;
    await api('/api/action', 'POST', { action });
  });
});

// Start passive polling so the enemy moves when idle
polling = setInterval(poll, 400);

