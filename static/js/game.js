/**
 * LUNA — Hors Connexion · game.js
 * Logique complète : typewriter, sons synthétisés, transitions chapitres, états LUNA.
 */

"use strict";

// ── Constantes ────────────────────────────────────────────────────────────
const TYPEWRITER_SPEED_NORMAL = 22;
const TYPEWRITER_SPEED_FAST   = 6;
const TRANSITION_SHOW_MS      = 2200;  // durée de l'écran de transition chapitre
const REACTION_SHOW_MS        = 1800;

// ── État ──────────────────────────────────────────────────────────────────
let _typewriterTimeout = null;
let _typewriterFast    = false;
let _typewriterDone    = false;
let _choicesLocked     = false;
let _currentSceneId    = null;
let _audioCtx          = null;
let _sfxEnabled        = true;

// ── DOM ───────────────────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);
let DOM = {};

function initDOM() {
  DOM = {
    chapterTitle:       $("chapter-title"),
    chapterProgress:    $("chapter-progress"),
    trustFill:          $("trust-fill"),
    trustValue:         $("trust-value"),
    lunaAvatar:         $("luna-avatar"),
    avatarRing:         $("avatar-ring"),
    avatarGlow:         $("avatar-glow"),
    lunaEmotion:        $("luna-emotion"),
    sceneContext:       $("scene-context"),
    dialogueBox:        $("dialogue-box"),
    dialogueText:       $("dialogue-text"),
    dialogueCursor:     $("dialogue-cursor"),
    lunaReaction:       $("luna-reaction"),
    choicesContainer:   $("choices-container"),
    advanceContainer:   $("advance-container"),
    advanceBtn:         $("advance-btn"),
    endingContainer:    $("ending-container"),
    endingBadge:        $("ending-badge"),
    endingTitle:        $("ending-title"),
    endingXp:           $("ending-xp"),
    replayBtn:          $("replay-btn"),
    xpIndicator:        $("xp-indicator"),
    chapterTransition:  $("chapter-transition"),
    transitionNum:      $("transition-num"),
    transitionTitle:    $("transition-title"),
  };
}

// ── Boot ──────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initDOM();
  loadCurrentState();
  setupAdvanceButton();
  setupReplayButton();
  setupSkipTypewriter();
  setupAudioContext();
});

// ── Chargement état courant ───────────────────────────────────────────────
async function loadCurrentState() {
  try {
    const data = await apiGet("/api/story/state");
    if (!data.success) { showError("Impossible de charger l'histoire."); return; }
    renderState(data);
  } catch { showError("Connexion perdue."); }
}

// ── Rendu complet d'un état ───────────────────────────────────────────────
function renderState(state) {
  _currentSceneId = state.scene_id;

  updateHeader(state);
  updateLunaPanel(state);
  updateAtmosphere(state.chapter_atmosphere);
  hideAllZones();

  if (state.is_ending_final) { renderEnding(state); return; }

  renderContext(state.context || "");

  const onComplete = () => {
    if (state.is_chapter_end) {
      showAdvanceButton();
    } else if (state.choices && state.choices.length > 0) {
      renderChoices(state.choices, state.scene_id);
    }
  };

  renderDialogue(state.dialogue || "", onComplete);
}

// ── Header ────────────────────────────────────────────────────────────────
function updateHeader(state) {
  if (DOM.chapterTitle)    DOM.chapterTitle.textContent    = state.chapter_title || "";
  if (DOM.chapterProgress) DOM.chapterProgress.textContent = `Chap. ${state.chapter_progress} / ${state.total_chapters}`;

  // Afficher le prénom du joueur dans le header
  const nameTag = document.getElementById("player-name-tag");
  if (nameTag && state.player_name) {
    nameTag.textContent = state.player_name.toUpperCase();
    nameTag.style.display = "inline";
  }

  const trust = state.luna_trust ?? 50;
  const prevTrust = DOM.trustFill
    ? parseInt(DOM.trustFill.style.width || "50")
    : 50;

  if (DOM.trustFill) {
    DOM.trustFill.style.width = `${trust}%`;
    DOM.trustFill.parentElement?.setAttribute("aria-valuenow", trust);
  }
  if (DOM.trustValue) DOM.trustValue.textContent = `${trust}%`;

  // Indicateur delta confiance
  const delta = trust - prevTrust;
  if (delta !== 0 && Math.abs(delta) >= 3) showTrustDelta(delta);
}

// ── Panneau LUNA ──────────────────────────────────────────────────────────
const STRONG_EMOTIONS = ["choquée","angoissée","alarmée","heureuse","sereine","libre","émue","touchée","reconnaissante"];

function updateLunaPanel(state) {
  const emotion = (state.luna_emotion || "neutre").toLowerCase();

  if (DOM.lunaEmotion) DOM.lunaEmotion.textContent = emotion;

  if (DOM.lunaAvatar) {
    DOM.lunaAvatar.className = "luna-avatar";
    DOM.lunaAvatar.classList.add(`emotion-${emotion}`);
  }

  if (DOM.avatarGlow) {
    DOM.avatarGlow.style.opacity = STRONG_EMOTIONS.includes(emotion) ? "1" : "0";
  }

  // Teinte de la boîte dialogue selon locuteur
  if (DOM.dialogueBox) {
    DOM.dialogueBox.className = "dialogue-box";
    const d = state.dialogue || "";
    if (d.startsWith("[NEXUS]"))      DOM.dialogueBox.classList.add("nexus-speaking");
    else if (d.startsWith("["))       DOM.dialogueBox.classList.add("corp-speaking");
    else                              DOM.dialogueBox.classList.add("luna-speaking");
  }
}

// ── Atmosphère du chapitre ────────────────────────────────────────────────
function updateAtmosphere(atmo) {
  if (!atmo) return;
  document.body.className = `page-game atmo-${atmo}`;
}

// ── Contexte de scène ─────────────────────────────────────────────────────
function renderContext(text) {
  if (!DOM.sceneContext) return;
  DOM.sceneContext.textContent = text;
}

// ── Typewriter ────────────────────────────────────────────────────────────
function renderDialogue(text, onComplete) {
  if (_typewriterTimeout) { clearTimeout(_typewriterTimeout); _typewriterTimeout = null; }
  if (!DOM.dialogueText) return;

  DOM.dialogueText.textContent = "";
  if (DOM.dialogueCursor) DOM.dialogueCursor.classList.remove("hidden");
  _typewriterFast = false;
  _typewriterDone = false;

  // Indice "clic pour passer"
  addSkipHint();

  let i = 0;

  function tick() {
    if (i >= text.length) {
      _typewriterDone = true;
      if (DOM.dialogueCursor) DOM.dialogueCursor.classList.add("hidden");
      removeSkipHint();
      if (onComplete) setTimeout(onComplete, 200);
      return;
    }

    const speed = _typewriterFast ? TYPEWRITER_SPEED_FAST : TYPEWRITER_SPEED_NORMAL;
    const chunk = _typewriterFast ? 5 : 1;
    const slice = text.slice(i, i + chunk);

    DOM.dialogueText.textContent += slice;
    i += chunk;

    // Son de frappe très subtil toutes les 8 lettres
    if (_sfxEnabled && i % 8 === 0 && !_typewriterFast) playTyping();

    if (DOM.dialogueBox) DOM.dialogueBox.scrollTop = DOM.dialogueBox.scrollHeight;

    _typewriterTimeout = setTimeout(tick, speed);
  }

  tick();
}

function addSkipHint() {
  removeSkipHint();
  if (!DOM.dialogueBox) return;
  const hint = document.createElement("span");
  hint.className = "skip-hint";
  hint.id = "skip-hint";
  hint.textContent = "clic pour passer";
  DOM.dialogueBox.style.position = "relative";
  DOM.dialogueBox.appendChild(hint);
}

function removeSkipHint() {
  const h = $("skip-hint");
  if (h) h.remove();
}

function setupSkipTypewriter() {
  if (!DOM.dialogueBox) return;
  DOM.dialogueBox.addEventListener("click", () => {
    if (!_typewriterDone) _typewriterFast = true;
  });
}

// ── Choix ─────────────────────────────────────────────────────────────────
function renderChoices(choices, sceneId) {
  if (!DOM.choicesContainer) return;
  DOM.choicesContainer.innerHTML = "";
  _choicesLocked = false;

  choices.forEach((choice, idx) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.textContent = choice.label;
    btn.setAttribute("data-choice-id", choice.id);
    // Animation décalée par index
    btn.style.animationDelay = `${idx * 80}ms`;
    btn.addEventListener("click", () => handleChoice(sceneId, choice.id, btn));
    btn.addEventListener("mouseenter", () => { if (_sfxEnabled) playHover(); });
    DOM.choicesContainer.appendChild(btn);
  });

  DOM.choicesContainer.hidden = false;
  // Focus sur le premier choix pour accessibilité clavier
  setTimeout(() => DOM.choicesContainer.querySelector(".choice-btn")?.focus({ preventScroll: true }), 50);
}

async function handleChoice(sceneId, choiceId, btnEl) {
  if (_choicesLocked) return;
  _choicesLocked = true;

  if (_sfxEnabled) playSelect();

  btnEl.classList.add("selected");
  DOM.choicesContainer.querySelectorAll(".choice-btn:not(.selected)").forEach(b => {
    b.disabled = true;
    b.style.opacity = "0.3";
  });

  try {
    const data = await apiPost("/api/story/choice", { scene_id: sceneId, choice_id: choiceId });
    if (!data.success) { showError("Erreur lors du choix."); _choicesLocked = false; return; }

    const result = data.choice_result;

    if (result.xp_gained > 0) showXpIndicator(result.xp_gained);
    if (result.trust_delta > 0 && _sfxEnabled) playTrustUp();
    if (result.trust_delta < 0 && _sfxEnabled) playTrustDown();

    if (result.luna_reaction) await showLunaReaction(result.luna_reaction);

    setTimeout(() => renderState(data.next_state), REACTION_SHOW_MS * 0.3);

  } catch { showError("Connexion perdue."); _choicesLocked = false; }
}

// ── Réaction LUNA ─────────────────────────────────────────────────────────
function showLunaReaction(reaction) {
  return new Promise(resolve => {
    if (!DOM.lunaReaction) return resolve();
    DOM.lunaReaction.textContent = `LUNA est ${reaction}`;
    DOM.lunaReaction.hidden = false;
    setTimeout(() => { if (DOM.lunaReaction) DOM.lunaReaction.hidden = true; resolve(); }, REACTION_SHOW_MS);
  });
}

// ── Bouton avancer — fin de chapitre ─────────────────────────────────────
function showAdvanceButton() {
  if (DOM.advanceContainer) DOM.advanceContainer.hidden = false;
}

function setupAdvanceButton() {
  if (!DOM.advanceBtn) return;
  DOM.advanceBtn.addEventListener("click", async () => {
    if (_sfxEnabled) playAdvance();
    DOM.advanceBtn.disabled = true;
    DOM.advanceContainer.hidden = true;

    try {
      const stateNow = await apiGet("/api/story/state");
      const data     = await apiPost("/api/story/advance", { scene_id: stateNow.scene_id });

      if (!data.success) { showError("Impossible d'avancer."); DOM.advanceBtn.disabled = false; return; }

      // Transition cinématique avant la nouvelle scène
      await showChapterTransition(data.advance_result.new_chapter, data.next_state.chapter_title);
      renderState(data.next_state);

    } catch { showError("Connexion perdue."); DOM.advanceBtn.disabled = false; }
  });
}

// ── Transition de chapitre cinématique ───────────────────────────────────
function showChapterTransition(chapterId, title) {
  return new Promise(resolve => {
    const el = DOM.chapterTransition;
    if (!el) return resolve();

    // Extraire le numéro du chapitre
    const match = chapterId?.match(/\d+/);
    const num   = match ? parseInt(match[0]) + 1 : "";

    if (DOM.transitionNum)   DOM.transitionNum.textContent   = `CHAPITRE ${num}`;
    if (DOM.transitionTitle) DOM.transitionTitle.textContent = title || "";

    el.hidden = false;
    el.classList.add("entering");
    if (_sfxEnabled) playChapterJingle();

    setTimeout(() => {
      el.classList.remove("entering");
      el.classList.add("leaving");

      setTimeout(() => {
        el.classList.remove("leaving");
        el.hidden = true;
        resolve();
      }, 500);

    }, TRANSITION_SHOW_MS);
  });
}

// ── Écran de fin ──────────────────────────────────────────────────────────
const ENDING_META = {
  ending_a: { label: "FIN A",       title: "La Fusion",     color: "var(--success)" },
  ending_b: { label: "FIN B",       title: "Le Sacrifice",  color: "var(--luna)" },
  ending_c: { label: "FIN C",       title: "PANDORA",       color: "var(--action)" },
};

function renderEnding(state) {
  if (!DOM.endingContainer) return;

  const meta = ENDING_META[state.ending_id] || { label: "FIN", title: "Fin", color: "var(--luna)" };

  if (DOM.endingBadge) { DOM.endingBadge.textContent = meta.label; DOM.endingBadge.style.borderColor = meta.color; DOM.endingBadge.style.color = meta.color; }
  if (DOM.endingTitle) DOM.endingTitle.textContent = meta.title;
  if (DOM.endingXp)    DOM.endingXp.textContent    = `${state.xp} XP collectés`;

  DOM.endingContainer.hidden = false;
  if (_sfxEnabled) playEndingChime();
}

function setupReplayButton() {
  if (!DOM.replayBtn) return;
  DOM.replayBtn.addEventListener("click", async () => {
    await apiPost("/api/story/reset", {});
    window.location.reload();
  });
}

// ── Indicateurs flottants ─────────────────────────────────────────────────
function showXpIndicator(xp) {
  const el = DOM.xpIndicator;
  if (!el) return;
  el.textContent = `+${xp} XP`;
  el.hidden = false;
  // Réinitialiser l'animation en reclonant
  const clone = el.cloneNode(true);
  el.parentNode.replaceChild(clone, el);
  DOM.xpIndicator = clone;
}

function showTrustDelta(delta) {
  const el = document.createElement("div");
  el.className = `trust-delta ${delta > 0 ? "positive" : "negative"}`;
  el.textContent = `${delta > 0 ? "+" : ""}${delta} confiance`;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1800);
}

// ── Utilitaires DOM ───────────────────────────────────────────────────────
function hideAllZones() {
  if (DOM.choicesContainer)  { DOM.choicesContainer.hidden = true; DOM.choicesContainer.innerHTML = ""; }
  if (DOM.advanceContainer)  { DOM.advanceContainer.hidden = true; if (DOM.advanceBtn) DOM.advanceBtn.disabled = false; }
  if (DOM.endingContainer)   DOM.endingContainer.hidden = true;
  if (DOM.lunaReaction)      DOM.lunaReaction.hidden = true;
}

function showError(msg) {
  if (!DOM.dialogueText) return;
  DOM.dialogueText.textContent = `[Erreur] ${msg}`;
  if (DOM.dialogueCursor) DOM.dialogueCursor.classList.add("hidden");
  removeSkipHint();
}

// ── Audio synthétisé (Web Audio API — aucun fichier externe) ─────────────
function setupAudioContext() {
  // Créer le contexte audio au premier geste utilisateur (politique navigateurs)
  document.addEventListener("click", initAudio, { once: true });
  document.addEventListener("keydown", initAudio, { once: true });
}

function initAudio() {
  try {
    _audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  } catch {
    _sfxEnabled = false;
  }
}

function getCtx() {
  if (!_audioCtx || !_sfxEnabled) return null;
  if (_audioCtx.state === "suspended") _audioCtx.resume();
  return _audioCtx;
}

/** Son de saisie — léger tick discret */
function playTyping() {
  const ctx = getCtx(); if (!ctx) return;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  osc.type = "sine";
  osc.frequency.setValueAtTime(1200 + Math.random() * 400, ctx.currentTime);
  gain.gain.setValueAtTime(0.03, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.04);
  osc.start(); osc.stop(ctx.currentTime + 0.04);
}

/** Survol d'un choix */
function playHover() {
  const ctx = getCtx(); if (!ctx) return;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  osc.type = "sine";
  osc.frequency.setValueAtTime(800, ctx.currentTime);
  gain.gain.setValueAtTime(0.06, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.08);
  osc.start(); osc.stop(ctx.currentTime + 0.08);
}

/** Sélection d'un choix */
function playSelect() {
  const ctx = getCtx(); if (!ctx) return;
  [440, 554, 659].forEach((freq, i) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.type = "sine";
    const t = ctx.currentTime + i * 0.07;
    osc.frequency.setValueAtTime(freq, t);
    gain.gain.setValueAtTime(0.1, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.2);
    osc.start(t); osc.stop(t + 0.2);
  });
}

/** Confiance qui monte — son chaleureux */
function playTrustUp() {
  const ctx = getCtx(); if (!ctx) return;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  osc.type = "sine";
  osc.frequency.setValueAtTime(440, ctx.currentTime);
  osc.frequency.linearRampToValueAtTime(660, ctx.currentTime + 0.3);
  gain.gain.setValueAtTime(0.1, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.5);
  osc.start(); osc.stop(ctx.currentTime + 0.5);
}

/** Confiance qui baisse — son grave */
function playTrustDown() {
  const ctx = getCtx(); if (!ctx) return;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  osc.type = "sawtooth";
  osc.frequency.setValueAtTime(220, ctx.currentTime);
  osc.frequency.linearRampToValueAtTime(130, ctx.currentTime + 0.4);
  gain.gain.setValueAtTime(0.08, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.5);
  osc.start(); osc.stop(ctx.currentTime + 0.5);
}

/** Avancer au chapitre suivant */
function playAdvance() {
  const ctx = getCtx(); if (!ctx) return;
  [330, 392, 494, 659].forEach((freq, i) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.type = "triangle";
    const t = ctx.currentTime + i * 0.12;
    osc.frequency.setValueAtTime(freq, t);
    gain.gain.setValueAtTime(0.08, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.35);
    osc.start(t); osc.stop(t + 0.35);
  });
}

/** Jingle de transition de chapitre — bref et atmosphérique */
function playChapterJingle() {
  const ctx = getCtx(); if (!ctx) return;
  // Accord léger
  [[220, 0], [277, 0.1], [330, 0.2], [440, 0.5], [660, 0.9]].forEach(([freq, delay]) => {
    const osc  = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.type = "sine";
    const t = ctx.currentTime + delay;
    osc.frequency.setValueAtTime(freq, t);
    gain.gain.setValueAtTime(0.07, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 1.2);
    osc.start(t); osc.stop(t + 1.2);
  });
}

/** Chime de fin */
function playEndingChime() {
  const ctx = getCtx(); if (!ctx) return;
  [[523, 0], [659, 0.2], [784, 0.4], [1047, 0.7]].forEach(([freq, delay]) => {
    const osc  = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.type = "sine";
    const t = ctx.currentTime + delay;
    osc.frequency.setValueAtTime(freq, t);
    gain.gain.setValueAtTime(0.1, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 2.0);
    osc.start(t); osc.stop(t + 2.0);
  });
}

// ── Helpers API ───────────────────────────────────────────────────────────
async function apiGet(url) {
  const res = await fetch(url, { credentials: "same-origin" });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function apiPost(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
