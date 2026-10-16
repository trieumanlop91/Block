"""
Block Puzzle 3D - Upgraded Graphics Edition
Run: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Block Puzzle 3D",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], .stDeployButton {display: none !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    html, body, [data-testid="stAppViewContainer"] {
        background: #152448 !important;
        overflow: hidden !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    iframe {border: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Block Puzzle 3D</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap');

  :root {
    --bg-top: #2a4a9e;
    --bg-mid: #1c3270;
    --bg-bot: #121f4a;
    --board-outer: #0a1628;
    --board-inner: #0d1b36;
    --cell: #142#if;
    --cell-border: rgba(255,255,255,0.04);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }

  html, body {
    width: 100%; height: 100%;
    background:
      radial-gradient(ellipse 120% 80% at 50% -10%, rgba(80,130,255,0.25) 0%, transparent 55%),
      linear-gradient(165deg, var(--bg-top) 0%, var(--bg-mid) 45%, var(--bg-bot) 100%);
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #fff;
    overflow: hidden;
    touch-action: none;
    user-select: none;
    -webkit-user-select: none;
  }

  #game {
    width: 100%; height: 100%;
    display: flex; flex-direction: column;
    align-items: center;
    padding: max(env(safe-area-inset-top), 8px) 10px max(env(safe-area-inset-bottom), 10px);
    max-width: 440px;
    margin: 0 auto;
    position: relative;
  }

  /* ========== TOP BAR ========== */
  .top-bar {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 4px 2px;
    z-index: 10;
  }
  .high-score {
    display: flex; align-items: center; gap: 7px;
    font-size: 22px; font-weight: 800;
    color: #ffd54f;
    text-shadow: 0 2px 4px rgba(0,0,0,0.45), 0 0 12px rgba(255,200,50,0.3);
  }
  .crown-svg {
    width: 30px; height: 30px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.4));
  }
  .icons { display: flex; gap: 8px; align-items: center; }
  .icon-btn {
    width: 38px; height: 38px;
    border-radius: 50%;
    background: linear-gradient(145deg, rgba(255,255,255,0.18), rgba(255,255,255,0.06));
    border: 1px solid rgba(255,255,255,0.22);
    box-shadow: 0 2px 8px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.15);
    display: flex; align-items: center; justify-content: center;
    cursor: pointer;
    font-size: 17px;
    color: #e8eeff;
    transition: transform 0.12s, background 0.15s;
  }
  .icon-btn:active { transform: scale(0.9); background: rgba(255,255,255,0.25); }

  /* ========== SCORE ========== */
  .score-display {
    font-size: 52px;
    font-weight: 900;
    letter-spacing: 0.5px;
    text-shadow:
      0 3px 0 rgba(0,0,0,0.25),
      0 6px 16px rgba(0,0,0,0.4),
      0 0 30px rgba(100,160,255,0.2);
    margin: 2px 0 14px;
    line-height: 1;
    background: linear-gradient(180deg, #ffffff 30%, #c8d8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* ========== BOARD ========== */
  .board-wrap {
    position: relative;
    width: min(90vw, 360px);
    aspect-ratio: 1;
    background: linear-gradient(160deg, #1a2d55 0%, #0c1830 100%);
    border-radius: 16px;
    padding: 7px;
    box-shadow:
      0 0 0 2px rgba(255,255,255,0.06),
      0 12px 32px rgba(0,0,0,0.5),
      0 4px 12px rgba(0,0,0,0.35),
      inset 0 1px 0 rgba(255,255,255,0.1),
      inset 0 -2px 6px rgba(0,0,0,0.3);
  }
  .board {
    width: 100%; height: 100%;
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: repeat(8, 1fr);
    gap: 3.5px;
    background: #0a1428;
    border-radius: 11px;
    padding: 3px;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.4);
  }
  .cell {
    background: linear-gradient(160deg, #152848 0%, #0f1e38 100%);
    border-radius: 5px;
    border: 1px solid rgba(255,255,255,0.03);
    position: relative;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.25);
  }

  /* ========== 3D BLOCK ========== */
  .block {
    width: 100%; height: 100%;
    border-radius: 5px;
    position: relative;
    overflow: hidden;
    transform: translateZ(0);
  }
  /* Top highlight face */
  .block::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 42%;
    border-radius: 5px 5px 40% 40%;
    background: linear-gradient(180deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.12) 60%, transparent 100%);
    pointer-events: none;
    z-index: 2;
  }
  /* Bottom shadow face */
  .block::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 28%;
    border-radius: 40% 40% 5px 5px;
    background: linear-gradient(0deg, rgba(0,0,0,0.35) 0%, transparent 100%);
    pointer-events: none;
    z-index: 2;
  }
  /* Side bevel via box-shadow */
  .block {
    box-shadow:
      inset 2px 0 3px rgba(255,255,255,0.2),
      inset -2px 0 4px rgba(0,0,0,0.25),
      inset 0 2px 2px rgba(255,255,255,0.25),
      inset 0 -3px 4px rgba(0,0,0,0.3),
      0 2px 5px rgba(0,0,0,0.35),
      0 1px 2px rgba(0,0,0,0.2);
  }

  /* Color variants – richer gradients */
  .c-blue {
    background:
      linear-gradient(145deg, #64b5f6 0%, #1e88e5 40%, #1565c0 100%);
  }
  .c-yellow {
    background:
      linear-gradient(145deg, #fff176 0%, #ffd54f 35%, #f9a825 100%);
  }
  .c-red {
    background:
      linear-gradient(145deg, #ef9a9a 0%, #e53935 40%, #c62828 100%);
  }
  .c-green {
    background:
      linear-gradient(145deg, #81c784 0%, #43a047 40%, #2e7d32 100%);
  }
  .c-purple {
    background:
      linear-gradient(145deg, #ce93d8 0%, #ab47bc 40%, #7b1fa2 100%);
  }
  .c-orange {
    background:
      linear-gradient(145deg, #ffcc80 0%, #ffa726 40%, #ef6c00 100%);
  }
  .c-cyan {
    background:
      linear-gradient(145deg, #80deea 0%, #26c6da 40%, #00838f 100%);
  }

  /* Glow accent per color */
  .c-blue   { filter: saturate(1.1); }
  .c-yellow { filter: saturate(1.15) brightness(1.05); }
  .c-red    { filter: saturate(1.1); }
  .c-green  { filter: saturate(1.1); }
  .c-purple { filter: saturate(1.1); }
  .c-orange { filter: saturate(1.12); }
  .c-cyan   { filter: saturate(1.1); }

  /* Preview ghost */
  .preview .block {
    opacity: 0.4;
    filter: brightness(1.3) !important;
    box-shadow:
      inset 0 0 0 2px rgba(255,255,255,0.5),
      0 0 12px rgba(255,255,255,0.25);
  }
  .preview .block::before,
  .preview .block::after { opacity: 0.5; }

  /* Place bounce */
  .block.just-placed {
    animation: placeBounce 0.28s cubic-bezier(0.34, 1.4, 0.64, 1);
  }
  @keyframes placeBounce {
    0%   { transform: scale(0.6); opacity: 0.5; }
    60%  { transform: scale(1.12); }
    100% { transform: scale(1); opacity: 1; }
  }

  /* Clear animation */
  .clearing .block {
    animation: clearBurst 0.4s ease-out forwards;
  }
  @keyframes clearBurst {
    0%   { transform: scale(1); opacity: 1; filter: brightness(1); }
    25%  { transform: scale(1.2); filter: brightness(1.8); }
    100% { transform: scale(0); opacity: 0; filter: brightness(2.5); }
  }

  /* ========== TRAY ========== */
  .tray {
    width: min(90vw, 360px);
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 20px;
    gap: 6px;
    min-height: 118px;
  }
  .piece-slot {
    width: 108px;
    height: 108px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    border-radius: 14px;
    background: linear-gradient(160deg, rgba(0,0,0,0.18), rgba(0,0,0,0.08));
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.2);
  }
  .piece {
    display: grid;
    gap: 3px;
    cursor: grab;
    touch-action: none;
    transition: transform 0.15s cubic-bezier(0.34, 1.4, 0.64, 1);
  }
  .piece:active, .piece.dragging { cursor: grabbing; transform: scale(1.05); }
  .piece .pblock {
    width: 24px; height: 24px;
    border-radius: 4px;
    position: relative;
    overflow: hidden;
    box-shadow:
      inset 1px 0 2px rgba(255,255,255,0.25),
      inset -1px 0 3px rgba(0,0,0,0.25),
      inset 0 1px 2px rgba(255,255,255,0.3),
      inset 0 -2px 3px rgba(0,0,0,0.3),
      0 2px 4px rgba(0,0,0,0.3);
  }
  .piece .pblock::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 42%;
    border-radius: 4px 4px 40% 40%;
    background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, transparent 100%);
    pointer-events: none;
  }
  .piece .pblock::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 25%;
    background: linear-gradient(0deg, rgba(0,0,0,0.3), transparent);
    pointer-events: none;
  }

  /* Drag ghost */
  #ghost {
    position: fixed;
    pointer-events: none;
    z-index: 1000;
    display: none;
    filter: drop-shadow(0 10px 20px rgba(0,0,0,0.55));
    opacity: 0.92;
  }
  #ghost .piece { transform: scale(1.2); }

  /* ========== OVERLAYS ========== */
  .overlay {
    position: absolute;
    inset: 0;
    background: rgba(8, 14, 32, 0.88);
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 50;
    border-radius: 16px;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
  }
  .overlay.show { display: flex; }
  .overlay h2 {
    font-size: 38px;
    font-weight: 900;
    margin-bottom: 6px;
    background: linear-gradient(180deg, #fff 20%, #a0b8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
  }
  .overlay p { font-size: 20px; margin-bottom: 28px; color: #b0c0e8; font-weight: 700; }
  .btn {
    padding: 15px 40px;
    font-size: 18px;
    font-weight: 800;
    font-family: inherit;
    border: none;
    border-radius: 32px;
    background: linear-gradient(145deg, #6eafff, #2979ff 50%, #1565c0);
    color: #fff;
    cursor: pointer;
    box-shadow:
      0 4px 16px rgba(41,121,255,0.5),
      inset 0 1px 0 rgba(255,255,255,0.3),
      inset 0 -2px 4px rgba(0,0,0,0.2);
    transition: transform 0.12s;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
  }
  .btn:active { transform: scale(0.95); }
  .btn.secondary {
    background: linear-gradient(145deg, #90a4ae, #607d8b 50%, #455a64);
    box-shadow: 0 4px 14px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.2);
    margin-top: 12px;
  }

  /* Score popup */
  .score-popup {
    position: absolute;
    font-weight: 900;
    font-size: 24px;
    color: #fff59d;
    text-shadow: 0 2px 8px rgba(0,0,0,0.6), 0 0 12px rgba(255,235,100,0.5);
    pointer-events: none;
    animation: floatUp 0.95s ease-out forwards;
    z-index: 20;
  }
  @keyframes floatUp {
    0%   { opacity: 1; transform: translateY(0) scale(0.8); }
    20%  { transform: translateY(-10px) scale(1.2); }
    100% { opacity: 0; transform: translateY(-55px) scale(1.1); }
  }

  /* Combo banner */
  .combo-banner {
    position: absolute;
    top: 42%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    font-size: 32px;
    font-weight: 900;
    color: #ffeb3b;
    text-shadow:
      0 0 16px rgba(255,235,59,0.7),
      0 3px 8px rgba(0,0,0,0.5),
      0 0 40px rgba(255,200,0,0.3);
    z-index: 25;
    pointer-events: none;
    white-space: nowrap;
    letter-spacing: 1px;
  }
  .combo-banner.show {
    animation: comboPop 0.9s cubic-bezier(0.34, 1.4, 0.64, 1) forwards;
  }
  @keyframes comboPop {
    0%   { transform: translate(-50%, -50%) scale(0) rotate(-8deg); opacity: 0; }
    25%  { transform: translate(-50%, -50%) scale(1.35) rotate(3deg); opacity: 1; }
    55%  { transform: translate(-50%, -50%) scale(1.1) rotate(-1deg); opacity: 1; }
    100% { transform: translate(-50%, -50%) scale(0.85) rotate(0deg); opacity: 0; }
  }

  /* Particle sparkles on clear */
  .spark {
    position: absolute;
    width: 6px; height: 6px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 30;
    animation: sparkFly 0.5s ease-out forwards;
  }
  @keyframes sparkFly {
    0%   { opacity: 1; transform: translate(0,0) scale(1); }
    100% { opacity: 0; transform: translate(var(--sx), var(--sy)) scale(0); }
  }
</style>
</head>
<body>
<div id="game">
  <div class="top-bar">
    <div class="high-score">
      <svg class="crown-svg" viewBox="0 0 64 64" fill="none">
        <defs>
          <linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#ffe082"/>
            <stop offset="50%" stop-color="#ffc107"/>
            <stop offset="100%" stop-color="#ff8f00"/>
          </linearGradient>
        </defs>
        <path d="M8 44 L12 20 L24 36 L32 12 L40 36 L52 20 L56 44 Z" fill="url(#cg)" stroke="#e65100" stroke-width="2" stroke-linejoin="round"/>
        <rect x="10" y="44" width="44" height="10" rx="3" fill="url(#cg)" stroke="#e65100" stroke-width="1.5"/>
        <circle cx="12" cy="18" r="4" fill="#fff59d" stroke="#ff8f00" stroke-width="1.5"/>
        <circle cx="32" cy="10" r="4.5" fill="#fff59d" stroke="#ff8f00" stroke-width="1.5"/>
        <circle cx="52" cy="18" r="4" fill="#fff59d" stroke="#ff8f00" stroke-width="1.5"/>
      </svg>
      <span id="high-score">0</span>
    </div>
    <div class="icons">
      <div class="icon-btn" id="btn-sound" title="Sound">🔊</div>
      <div class="icon-btn" id="btn-pause" title="Pause">⏸</div>
      <div class="icon-btn" id="btn-restart" title="Restart">↺</div>
    </div>
  </div>

  <div class="score-display" id="score">0</div>

  <div class="board-wrap" id="board-wrap">
    <div class="board" id="board"></div>
    <div class="overlay" id="gameover-overlay">
      <h2>Game Over</h2>
      <p>Score: <span id="final-score">0</span></p>
      <button class="btn" id="btn-play-again">Play Again</button>
    </div>
    <div class="overlay" id="pause-overlay">
      <h2>Paused</h2>
      <button class="btn" id="btn-resume">Resume</button>
      <button class="btn secondary" id="btn-restart2">Restart</button>
    </div>
    <div class="combo-banner" id="combo-banner"></div>
  </div>

  <div class="tray" id="tray"></div>
</div>

<div id="ghost"></div>

<script>
(function() {
  const GRID = 8;
  const COLORS = ['blue','yellow','red','green','purple','orange','cyan'];
  const COLOR_CLASS = {
    blue: 'c-blue', yellow: 'c-yellow', red: 'c-red',
    green: 'c-green', purple: 'c-purple', orange: 'c-orange', cyan: 'c-cyan'
  };
  const COLOR_HEX = {
    blue: '#1e88e5', yellow: '#ffd54f', red: '#e53935',
    green: '#43a047', purple: '#ab47bc', orange: '#ffa726', cyan: '#26c6da'
  };

  const SHAPES = [
    [[0,0]],
    [[0,0],[0,1]],
    [[0,0],[1,0]],
    [[0,0],[0,1],[0,2]],
    [[0,0],[1,0],[2,0]],
    [[0,0],[0,1],[1,0]],
    [[0,0],[0,1],[1,1]],
    [[0,0],[0,1],[1,0],[1,1]],
    [[0,0],[0,1],[0,2],[0,3]],
    [[0,0],[1,0],[2,0],[3,0]],
    [[0,0],[1,0],[2,0],[2,1]],
    [[0,1],[1,1],[2,1],[2,0]],
    [[0,0],[0,1],[0,2],[1,2]],
    [[0,0],[1,0],[1,1],[1,2]],
    [[0,0],[0,1],[1,1],[2,1]],
    [[0,1],[1,0],[1,1],[1,2]],
    [[0,0],[1,0],[2,0],[1,1]],
    [[0,1],[1,0],[1,1],[2,1]],
    [[0,0],[0,1],[0,2],[1,0],[1,1]],
    [[0,0],[0,1],[1,0],[1,1],[2,0]],
    [[0,0],[1,0],[2,0],[2,1],[2,2]],
    [[0,0],[0,1],[0,2],[1,2],[2,2]],
    [[0,2],[1,0],[1,1],[1,2],[2,2]],
    [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1]],
    [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]],
    [[0,0],[0,1],[0,2],[1,1]],
    [[0,1],[1,0],[1,1],[1,2],[2,1]],
  ];

  let grid = Array.from({length: GRID}, () => Array(GRID).fill(null));
  let score = 0;
  let highScore = parseInt(localStorage.getItem('bp3d_high') || '0', 10);
  let pieces = [null, null, null];
  let soundOn = true;
  let paused = false;
  let gameOver = false;
  let drag = null;

  const boardEl = document.getElementById('board');
  const trayEl = document.getElementById('tray');
  const scoreEl = document.getElementById('score');
  const highEl = document.getElementById('high-score');
  const ghostEl = document.getElementById('ghost');
  const gameoverEl = document.getElementById('gameover-overlay');
  const pauseEl = document.getElementById('pause-overlay');
  const comboEl = document.getElementById('combo-banner');
  const finalScoreEl = document.getElementById('final-score');
  const boardWrap = document.getElementById('board-wrap');

  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  let actx = null;
  function ensureAudio() { if (!actx) actx = new AudioCtx(); }
  function beep(freq, dur, type='square', vol=0.08) {
    if (!soundOn) return;
    try {
      ensureAudio();
      const o = actx.createOscillator();
      const g = actx.createGain();
      o.type = type; o.frequency.value = freq;
      g.gain.value = vol;
      o.connect(g); g.connect(actx.destination);
      o.start();
      g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + dur);
      o.stop(actx.currentTime + dur);
    } catch(e) {}
  }
  function sfxPlace() { beep(360, 0.07, 'triangle', 0.07); }
  function sfxClear() {
    beep(480, 0.1, 'sine', 0.1);
    setTimeout(() => beep(640, 0.12, 'sine', 0.09), 70);
    setTimeout(() => beep(820, 0.15, 'sine', 0.07), 150);
  }
  function sfxCombo() {
    beep(400, 0.08, 'square', 0.09);
    setTimeout(() => beep(560, 0.1, 'square', 0.09), 90);
    setTimeout(() => beep(720, 0.12, 'square', 0.1), 180);
    setTimeout(() => beep(900, 0.18, 'sine', 0.08), 280);
  }
  function sfxGameOver() {
    beep(220, 0.25, 'sawtooth', 0.1);
    setTimeout(() => beep(160, 0.35, 'sawtooth', 0.08), 220);
  }

  function buildBoard() {
    boardEl.innerHTML = '';
    for (let r = 0; r < GRID; r++) {
      for (let c = 0; c < GRID; c++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.r = r;
        cell.dataset.c = c;
        boardEl.appendChild(cell);
      }
    }
  }

  function renderGrid(justPlaced) {
    const cells = boardEl.children;
    for (let r = 0; r < GRID; r++) {
      for (let c = 0; c < GRID; c++) {
        const idx = r * GRID + c;
        const cell = cells[idx];
        cell.innerHTML = '';
        cell.classList.remove('preview', 'clearing');
        const color = grid[r][c];
        if (color) {
          const b = document.createElement('div');
          b.className = 'block ' + COLOR_CLASS[color];
          if (justPlaced && justPlaced.some(([pr, pc]) => pr === r && pc === c)) {
            b.classList.add('just-placed');
          }
          cell.appendChild(b);
        }
      }
    }
  }

  function randomShape() {
    return SHAPES[Math.floor(Math.random() * SHAPES.length)].map(p => [...p]);
  }
  function randomColor() {
    return COLORS[Math.floor(Math.random() * COLORS.length)];
  }

  function newPieceSet() {
    pieces = [0,1,2].map(() => ({ shape: randomShape(), color: randomColor() }));
    renderTray();
  }

  function shapeBounds(shape) {
    let maxR = 0, maxC = 0;
    shape.forEach(([r,c]) => { maxR = Math.max(maxR, r); maxC = Math.max(maxC, c); });
    return { rows: maxR + 1, cols: maxC + 1 };
  }

  function renderTray() {
    trayEl.innerHTML = '';
    pieces.forEach((p, idx) => {
      const slot = document.createElement('div');
      slot.className = 'piece-slot';
      if (!p) { trayEl.appendChild(slot); return; }
      const { rows, cols } = shapeBounds(p.shape);
      const piece = document.createElement('div');
      piece.className = 'piece';
      piece.dataset.idx = idx;
      piece.style.gridTemplateColumns = `repeat(${cols}, 24px)`;
      piece.style.gridTemplateRows = `repeat(${rows}, 24px)`;
      const occupied = new Set(p.shape.map(([r,c]) => r + ',' + c));
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          if (occupied.has(r + ',' + c)) {
            const b = document.createElement('div');
            b.className = 'pblock ' + COLOR_CLASS[p.color];
            b.style.gridRow = r + 1;
            b.style.gridColumn = c + 1;
            piece.appendChild(b);
          }
        }
      }
      piece.addEventListener('pointerdown', onPointerDown);
      slot.appendChild(piece);
      trayEl.appendChild(slot);
    });
  }

  function canPlace(shape, baseR, baseC) {
    for (const [dr, dc] of shape) {
      const r = baseR + dr, c = baseC + dc;
      if (r < 0 || r >= GRID || c < 0 || c >= GRID) return false;
      if (grid[r][c]) return false;
    }
    return true;
  }

  function place(shape, color, baseR, baseC) {
    const placed = [];
    for (const [dr, dc] of shape) {
      grid[baseR + dr][baseC + dc] = color;
      placed.push([baseR + dr, baseC + dc]);
    }
    return placed;
  }

  function spawnSparks(cellEl, color) {
    const rect = cellEl.getBoundingClientRect();
    const wrapRect = boardWrap.getBoundingClientRect();
    const cx = rect.left + rect.width / 2 - wrapRect.left;
    const cy = rect.top + rect.height / 2 - wrapRect.top;
    const hex = COLOR_HEX[color] || '#fff';
    for (let i = 0; i < 5; i++) {
      const s = document.createElement('div');
      s.className = 'spark';
      s.style.background = hex;
      s.style.left = cx + 'px';
      s.style.top = cy + 'px';
      s.style.boxShadow = `0 0 6px ${hex}`;
      const angle = (Math.PI * 2 * i) / 5 + Math.random() * 0.5;
      const dist = 18 + Math.random() * 22;
      s.style.setProperty('--sx', Math.cos(angle) * dist + 'px');
      s.style.setProperty('--sy', Math.sin(angle) * dist + 'px');
      boardWrap.appendChild(s);
      setTimeout(() => s.remove(), 500);
    }
  }

  function clearLines() {
    const fullRows = [];
    const fullCols = [];
    for (let r = 0; r < GRID; r++) {
      if (grid[r].every(cell => cell !== null)) fullRows.push(r);
    }
    for (let c = 0; c < GRID; c++) {
      let full = true;
      for (let r = 0; r < GRID; r++) if (!grid[r][c]) { full = false; break; }
      if (full) fullCols.push(c);
    }
    if (fullRows.length === 0 && fullCols.length === 0) return 0;

    const cells = boardEl.children;
    const clearedSet = new Set();
    fullRows.forEach(r => {
      for (let c = 0; c < GRID; c++) {
        const idx = r * GRID + c;
        cells[idx].classList.add('clearing');
        clearedSet.add(idx);
        if (grid[r][c]) spawnSparks(cells[idx], grid[r][c]);
      }
    });
    fullCols.forEach(c => {
      for (let r = 0; r < GRID; r++) {
        const idx = r * GRID + c;
        cells[idx].classList.add('clearing');
        if (!clearedSet.has(idx) && grid[r][c]) spawnSparks(cells[idx], grid[r][c]);
      }
    });

    setTimeout(() => {
      fullRows.forEach(r => { for (let c = 0; c < GRID; c++) grid[r][c] = null; });
      fullCols.forEach(c => { for (let r = 0; r < GRID; r++) grid[r][c] = null; });
      renderGrid();
    }, 320);

    return fullRows.length + fullCols.length;
  }

  function addScore(pts, x, y) {
    score += pts;
    scoreEl.textContent = score;
    if (score > highScore) {
      highScore = score;
      highEl.textContent = highScore;
      localStorage.setItem('bp3d_high', highScore);
    }
    if (x != null) {
      const pop = document.createElement('div');
      pop.className = 'score-popup';
      pop.textContent = '+' + pts;
      pop.style.left = x + 'px';
      pop.style.top = y + 'px';
      boardWrap.appendChild(pop);
      setTimeout(() => pop.remove(), 950);
    }
  }

  function showCombo(n) {
    if (n < 2) return;
    const texts = { 2: 'COMBO x2!', 3: 'GREAT!', 4: 'AMAZING!', 5: 'UNREAL!' };
    comboEl.textContent = texts[n] || ('COMBO x' + n + '!');
    comboEl.classList.remove('show');
    void comboEl.offsetWidth;
    comboEl.classList.add('show');
    sfxCombo();
  }

  function anyPieceFits() {
    for (const p of pieces) {
      if (!p) continue;
      for (let r = 0; r < GRID; r++) {
        for (let c = 0; c < GRID; c++) {
          if (canPlace(p.shape, r, c)) return true;
        }
      }
    }
    return false;
  }

  function checkGameOver() {
    if (pieces.every(p => p === null)) newPieceSet();
    if (!anyPieceFits()) {
      gameOver = true;
      finalScoreEl.textContent = score;
      gameoverEl.classList.add('show');
      sfxGameOver();
    }
  }

  function getCellSize() {
    const cell = boardEl.querySelector('.cell');
    return cell ? cell.getBoundingClientRect().width : 40;
  }
  function boardRect() { return boardEl.getBoundingClientRect(); }

  function pointerToGrid(clientX, clientY, shape) {
    const rect = boardRect();
    const cellFull = rect.width / GRID;
    const { cols, rows } = shapeBounds(shape);
    const baseC = Math.round((clientX - rect.left) / cellFull - cols / 2);
    const baseR = Math.round((clientY - rect.top) / cellFull - rows / 2);
    return { r: baseR, c: baseC };
  }

  function showPreview(shape, color, baseR, baseC) {
    clearPreview();
    if (!canPlace(shape, baseR, baseC)) return;
    const cells = boardEl.children;
    for (const [dr, dc] of shape) {
      const r = baseR + dr, c = baseC + dc;
      const cell = cells[r * GRID + c];
      cell.classList.add('preview');
      const b = document.createElement('div');
      b.className = 'block ' + COLOR_CLASS[color];
      cell.appendChild(b);
    }
  }

  function clearPreview() {
    const cells = boardEl.children;
    for (let i = 0; i < cells.length; i++) {
      if (cells[i].classList.contains('preview')) {
        cells[i].classList.remove('preview');
        const real = grid[Math.floor(i / GRID)][i % GRID];
        cells[i].innerHTML = '';
        if (real) {
          const b = document.createElement('div');
          b.className = 'block ' + COLOR_CLASS[real];
          cells[i].appendChild(b);
        }
      }
    }
  }

  function onPointerDown(e) {
    if (paused || gameOver) return;
    e.preventDefault();
    const pieceEl = e.currentTarget;
    const idx = parseInt(pieceEl.dataset.idx, 10);
    const p = pieces[idx];
    if (!p) return;
    ensureAudio();
    drag = { shape: p.shape, color: p.color, slotIdx: idx };

    const { rows, cols } = shapeBounds(p.shape);
    ghostEl.innerHTML = '';
    const gPiece = document.createElement('div');
    gPiece.className = 'piece';
    gPiece.style.gridTemplateColumns = `repeat(${cols}, 30px)`;
    gPiece.style.gridTemplateRows = `repeat(${rows}, 30px)`;
    gPiece.style.gap = '3px';
    const occupied = new Set(p.shape.map(([r,c]) => r + ',' + c));
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        if (occupied.has(r + ',' + c)) {
          const b = document.createElement('div');
          b.className = 'pblock ' + COLOR_CLASS[p.color];
          b.style.width = '30px'; b.style.height = '30px';
          b.style.gridRow = r + 1; b.style.gridColumn = c + 1;
          gPiece.appendChild(b);
        }
      }
    }
    ghostEl.appendChild(gPiece);
    ghostEl.style.display = 'block';
    moveGhost(e.clientX, e.clientY);
    pieceEl.style.opacity = '0.25';
    pieceEl.setPointerCapture(e.pointerId);
    pieceEl.addEventListener('pointermove', onPointerMove);
    pieceEl.addEventListener('pointerup', onPointerUp);
    pieceEl.addEventListener('pointercancel', onPointerUp);
  }

  function moveGhost(x, y) {
    const { cols, rows } = shapeBounds(drag.shape);
    const w = cols * 33, h = rows * 33;
    ghostEl.style.left = (x - w / 2) + 'px';
    ghostEl.style.top = (y - h / 2 - 20) + 'px';
  }

  function onPointerMove(e) {
    if (!drag) return;
    e.preventDefault();
    moveGhost(e.clientX, e.clientY);
    const { r, c } = pointerToGrid(e.clientX, e.clientY, drag.shape);
    showPreview(drag.shape, drag.color, r, c);
  }

  function onPointerUp(e) {
    if (!drag) return;
    e.preventDefault();
    const pieceEl = e.currentTarget;
    pieceEl.releasePointerCapture(e.pointerId);
    pieceEl.removeEventListener('pointermove', onPointerMove);
    pieceEl.removeEventListener('pointerup', onPointerUp);
    pieceEl.removeEventListener('pointercancel', onPointerUp);
    pieceEl.style.opacity = '1';
    ghostEl.style.display = 'none';
    clearPreview();

    const { r, c } = pointerToGrid(e.clientX, e.clientY, drag.shape);
    if (canPlace(drag.shape, r, c)) {
      const placed = place(drag.shape, drag.color, r, c);
      const blocks = drag.shape.length;
      const br = boardRect();
      addScore(blocks, e.clientX - br.left, e.clientY - br.top);
      sfxPlace();
      pieces[drag.slotIdx] = null;
      renderTray();
      renderGrid(placed);

      setTimeout(() => {
        const lines = clearLines();
        if (lines > 0) {
          const bonus = lines === 1 ? 10 : lines === 2 ? 30 : lines === 3 ? 60 : 100;
          addScore(bonus * lines, br.width / 2, br.height / 2);
          showCombo(lines);
          sfxClear();
        }
        if (pieces.every(p => p === null)) newPieceSet();
        setTimeout(checkGameOver, 340);
      }, 60);
    }
    drag = null;
  }

  document.getElementById('btn-sound').addEventListener('click', () => {
    soundOn = !soundOn;
    document.getElementById('btn-sound').textContent = soundOn ? '🔊' : '🔇';
  });
  document.getElementById('btn-pause').addEventListener('click', () => {
    if (gameOver) return;
    paused = true;
    pauseEl.classList.add('show');
  });
  document.getElementById('btn-resume').addEventListener('click', () => {
    paused = false;
    pauseEl.classList.remove('show');
  });

  function restart() {
    grid = Array.from({length: GRID}, () => Array(GRID).fill(null));
    score = 0;
    scoreEl.textContent = '0';
    gameOver = false;
    paused = false;
    gameoverEl.classList.remove('show');
    pauseEl.classList.remove('show');
    seedBoard();
    newPieceSet();
    renderGrid();
  }
  document.getElementById('btn-restart').addEventListener('click', restart);
  document.getElementById('btn-restart2').addEventListener('click', restart);
  document.getElementById('btn-play-again').addEventListener('click', restart);

  function seedBoard() {
    const seeds = [
      [0,0,'blue'],[0,1,'yellow'],[0,3,'red'],[0,7,'yellow'],
      [1,7,'orange'],
      [2,3,'green'],[3,3,'green'],[4,3,'green'],
      [5,0,'blue'],[5,1,'yellow'],[5,2,'purple'],[5,3,'red'],
      [6,0,'orange'],[6,1,'red'],[6,2,'green'],[6,3,'red'],[6,5,'purple'],
      [7,0,'cyan'],[7,1,'blue'],[7,2,'yellow'],[7,3,'red'],
      [7,5,'cyan'],[7,6,'yellow'],[7,7,'blue'],
    ];
    seeds.forEach(([r,c,col]) => { grid[r][c] = col; });
  }

  highEl.textContent = highScore;
  buildBoard();
  seedBoard();
  newPieceSet();
  renderGrid();

  document.addEventListener('touchmove', e => { if (e.scale !== 1) e.preventDefault(); }, { passive: false });
  document.addEventListener('gesturestart', e => e.preventDefault());
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=740, scrolling=False)
