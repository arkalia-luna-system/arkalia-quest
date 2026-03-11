/**
 * LUNA — Hors Connexion · game.js
 * Logique complète : typewriter, sons synthétisés, transitions chapitres, états LUNA.
 */

"use strict";

// ── Constantes ────────────────────────────────────────────────────────────
const TYPEWRITER_SPEED_NORMAL = 14;  // Plus snappy pour un ado
const TYPEWRITER_SPEED_FAST   = 5;
const TRANSITION_SHOW_MS      = 2200;  // durée de l'écran de transition chapitre
const REACTION_SHOW_MS        = 1800;

// ── État ──────────────────────────────────────────────────────────────────
let _typewriterTimeout  = null;
let _typewriterFast     = false;
let _typewriterDone     = false;
let _choicesLocked      = false;
let _currentSceneId     = null;
let _currentChapterId   = null;
let _chapterFlags       = [];   // flags acquis dans le chapitre courant
let _positiveStreak     = 0;    // bons choix consécutifs
let _audioCtx           = null;
let _sfxEnabled         = localStorage.getItem("luna_sfx") !== "off";
let _ambientNodes       = [];     // oscillateurs du drone ambiant
let _ambientAtmo        = null;   // atmosphère courante

// Labels lisibles pour les flags — côté client
const FLAG_LABELS_JS = {
  // Début
  "accepted_chapter_0":       "Tu as accepté d'aider LUNA dès le début.",
  "reassured_luna":           "Tu as rassuré LUNA sur ses doutes.",
  // Exploration
  "looked_at_pandora":        "Tu as examiné PANDORA avant de le transférer.",
  "saw_luna_logs":            "Tu as découvert les logs de LUNA.",
  "questioned_pandora_early": "Tu as interrogé LUNA sur La Corp.",
  "knows_about_miroir":       "Tu connais le Projet Miroir.",
  // La Corp
  "listened_to_corp":         "Tu as écouté l'agent de La Corp.",
  "agreed_to_pause_luna":     "Tu as coupé le contact avec LUNA.",
  // NEXUS
  "listened_to_nexus":        "Tu as écouté NEXUS en premier.",
  "tried_nexus":              "Tu as tenté de convaincre NEXUS.",
  "nexus_considering":        "Tu as ébranlé les certitudes de NEXUS.",
  "nexus_helped":             "NEXUS a changé de camp pour vous.",
  "abandoned_nexus":          "Tu n'as pas attendu NEXUS.",
  // Choix finale
  "chose_pandora_public":     "Tu as opté pour rendre les données publiques.",
  "pandora_public":           "Tu as rendu PANDORA public.",
  // Chemins de fin
  "ending_a_path":            "Tu as suivi le chemin de la Fusion.",
  "ending_b_path":            "Tu as suivi le chemin du Sacrifice.",
  "ending_c_path":            "Tu as suivi le chemin de PANDORA.",
};

// Flags rares qui déclenchent un popup "Exploit débloqué"
const EXPLOIT_FLAGS = {
  "nexus_helped":             "NEXUS retournée",
  "nexus_considering":        "NEXUS ébranlée",
  "knows_about_miroir":       "Projet Miroir déchiffré",
  "pandora_public":           "PANDORA lâché dans la nature",
  "reassured_luna":           "Tu as su quoi dire",
  "saw_luna_logs":            "Archive LUNA infiltrée",
  "agreed_to_pause_luna":     "Contact coupé",
};

let _exploitTimeout = null;

function showExploitPopup(flagId) {
  const label = EXPLOIT_FLAGS[flagId];
  if (!label) return;
  const popup = document.getElementById("exploit-popup");
  const nameEl = document.getElementById("exploit-name");
  if (!popup || !nameEl) return;
  nameEl.textContent = label;
  popup.hidden = false;
  popup.classList.add("visible");
  if (_exploitTimeout) clearTimeout(_exploitTimeout);
  _exploitTimeout = setTimeout(() => {
    popup.classList.remove("visible");
    setTimeout(() => { popup.hidden = true; }, 500);
  }, 3000);
}

let _streakTimeout = null;

function showStreakPopup(count) {
  const popup = document.getElementById("streak-popup");
  const xEl   = document.getElementById("streak-x");
  if (!popup || !xEl) return;
  xEl.textContent = `×${count}`;
  popup.hidden = false;
  popup.classList.add("visible");
  if (_streakTimeout) clearTimeout(_streakTimeout);
  _streakTimeout = setTimeout(() => {
    popup.classList.remove("visible");
    setTimeout(() => { popup.hidden = true; }, 400);
  }, 1800);
}

// ── DOM ───────────────────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);
let DOM = {};

function initDOM() {
  DOM = {
    chapterTitle:        $("chapter-title"),
    chapterProgress:     $("chapter-progress"),
    playerNameTag:       $("player-name-tag"),
    xpHeader:            $("xp-header"),
    trustFill:           $("trust-fill"),
    trustValue:          $("trust-value"),
    lunaAvatar:          $("luna-avatar"),
    avatarRing:          $("avatar-ring"),
    avatarGlow:          $("avatar-glow"),
    lunaEmotion:         $("luna-emotion"),
    sceneContext:        $("scene-context"),
    dialogueBox:         $("dialogue-box"),
    dialogueText:        $("dialogue-text"),
    dialogueCursor:      $("dialogue-cursor"),
    lunaReaction:        $("luna-reaction"),
    choicesContainer:    $("choices-container"),
    advanceContainer:    $("advance-container"),
    advanceBtn:          $("advance-btn"),
    endingContainer:     $("ending-container"),
    endingIcon:          $("ending-icon"),
    endingBadge:         $("ending-badge"),
    endingTitle:         $("ending-title"),
    endingDescription:   $("ending-description"),
    endingTrust:         $("ending-trust"),
    endingXp:            $("ending-xp"),
    endingPersonalized:  $("ending-personalized"),
    endingParticles:     $("ending-particles"),
    replayBtn:           $("replay-btn"),
    shareBtn:            $("share-btn"),
    storyProgressFill:   $("story-progress-fill"),
    bootOverlay:         $("boot-overlay"),
    xpIndicator:         $("xp-indicator"),
    chapterTransition:   $("chapter-transition"),
    transitionNum:       $("transition-num"),
    transitionTitle:     $("transition-title"),
    transitionQuote:     $("transition-quote"),
  };
}

// ── Boot ──────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initDOM();
  showLoadingSkeleton();
  loadCurrentState();
  setupAdvanceButton();
  setupReplayButton();
  setupSkipTypewriter();
  setupTouchSkip();
  setupKeyboardShortcuts();
  setupAudioContext();
  setupSfxButton();
  setupFirstPlayTip();
  setupIdleEasterEgg();
  setupKonamiCode();
});

// ── Tooltip première visite ───────────────────────────────────────────────
function setupFirstPlayTip() {
  const seen = localStorage.getItem("luna_played");
  if (seen) return;

  const tip = document.getElementById("first-play-tip");
  if (!tip) return;

  // Afficher 3 secondes après le chargement initial (laisse le temps de lire le dialogue)
  setTimeout(() => {
    tip.hidden = false;
    tip.classList.add("tip-entering");
    setTimeout(() => tip.classList.remove("tip-entering"), 500);
  }, 3500);

  // Disparaît automatiquement après 12 secondes
  setTimeout(() => dismissFirstPlayTip(), 15500);
}

function dismissFirstPlayTip() {
  const tip = document.getElementById("first-play-tip");
  if (!tip || tip.hidden) return;
  tip.classList.add("tip-leaving");
  setTimeout(() => { tip.hidden = true; tip.classList.remove("tip-leaving"); }, 400);
  localStorage.setItem("luna_played", "1");
}

function setupSfxButton() {
  const btn = document.getElementById("sfx-btn");
  if (!btn) return;
  const update = () => {
    btn.textContent  = _sfxEnabled ? "🔊" : "🔇";
    btn.title        = _sfxEnabled ? "Couper le son" : "Activer le son";
    btn.style.opacity = _sfxEnabled ? "0.7" : "0.35";
  };
  update();
  btn.addEventListener("click", () => {
    _sfxEnabled = !_sfxEnabled;
    localStorage.setItem("luna_sfx", _sfxEnabled ? "on" : "off");
    update();
    if (_sfxEnabled && _ambientAtmo) startAmbientDrone(_ambientAtmo);
    else stopAmbientDrone(800);
  });
}

// ── Boot overlay ──────────────────────────────────────────────────────────
function hideBootOverlay() {
  const el = DOM.bootOverlay;
  if (!el || el.classList.contains("boot-done")) return;
  el.classList.add("boot-done");
  setTimeout(() => { el.hidden = true; }, 500);
}

// ── Skeleton de chargement ───────────────────────────────────────────────
function showLoadingSkeleton() {
  if (DOM.dialogueText) {
    DOM.dialogueText.innerHTML = '<span class="loading-skeleton-line"></span><span class="loading-skeleton-line short"></span>';
  }
  if (DOM.sceneContext) DOM.sceneContext.textContent = "Connexion au réseau LUNA…";
  if (DOM.choicesContainer) DOM.choicesContainer.hidden = true;
  if (DOM.advanceContainer) DOM.advanceContainer.hidden = true;
}

// ── Chargement état courant ───────────────────────────────────────────────
async function loadCurrentState() {
  try {
    const data = await apiGet("/api/story/state");
    if (!data.success) { hideBootOverlay(); showError("Impossible de charger l'histoire."); return; }
    renderState(data);
  } catch { hideBootOverlay(); showError("Connexion perdue."); }
}

// ── Rendu complet d'un état ───────────────────────────────────────────────
function renderState(state) {
  hideBootOverlay();

  // Réinitialiser les flags du chapitre si on change de chapitre
  if (state.chapter_id !== _currentChapterId) {
    _chapterFlags = [];
    _currentChapterId = state.chapter_id;
  }
  _currentSceneId = state.scene_id;

  updateHeader(state);
  updateLunaPanel(state);
  updateAtmosphere(state.chapter_atmosphere);
  hideAllZones();

  if (state.is_ending_final) { renderEnding(state); return; }

  renderContext(state.context || "");

  const onComplete = () => {
    if (state.is_chapter_end) {
      showAdvanceButton(state);
    } else if (state.choices && state.choices.length > 0) {
      renderChoices(state.choices, state.scene_id);
    }
  };

  renderDialogue(state.dialogue || "", onComplete);

  // Scroll vers la zone de dialogue sur mobile (petits écrans)
  if (window.innerWidth <= 640) {
    DOM.dialogueBox?.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// ── Header ────────────────────────────────────────────────────────────────
function updateHeader(state) {
  if (DOM.chapterTitle) DOM.chapterTitle.textContent = state.chapter_title || "";

  if (DOM.chapterProgress) {
    const sceneInfo = (state.scene_index && state.scene_total && !state.is_ending_final)
      ? ` · ${state.scene_index}/${state.scene_total}`
      : "";
    DOM.chapterProgress.textContent = `Chap. ${state.chapter_progress} / ${state.total_chapters}${sceneInfo}`;
  }

  // Barre de progression globale
  if (DOM.storyProgressFill && !state.is_ending_final) {
    const total   = state.total_chapters || 8;
    const chapPct = (state.chapter_progress || 0) / total;
    const scenePct = (state.scene_index && state.scene_total)
      ? (state.scene_index / state.scene_total) * (1 / total)
      : 0;
    const pct = Math.min(100, ((chapPct + scenePct) * 100)).toFixed(1);
    DOM.storyProgressFill.style.width = `${pct}%`;
  } else if (DOM.storyProgressFill && state.is_ending_final) {
    DOM.storyProgressFill.style.width = "100%";
  }

  // XP total dans le header (animé si changement)
  if (DOM.xpHeader) {
    const newXp = state.xp ?? 0;
    const oldXp = parseInt(DOM.xpHeader.dataset.xp || "0", 10);
    DOM.xpHeader.textContent = `${newXp} XP`;
    DOM.xpHeader.dataset.xp = newXp;
    if (newXp > oldXp && oldXp > 0) {
      DOM.xpHeader.classList.add("xp-gained");
      setTimeout(() => DOM.xpHeader?.classList.remove("xp-gained"), 600);
    }
  }

  // Prénom du joueur dans le header
  if (DOM.playerNameTag && state.player_name) {
    DOM.playerNameTag.textContent = state.player_name;
    DOM.playerNameTag.style.display = "inline";
  }

  const trust = state.luna_trust ?? 50;
  const prevTrust = DOM.trustFill
    ? parseInt(DOM.trustFill.style.width || "50")
    : 50;

  if (DOM.trustFill) {
    DOM.trustFill.style.width = `${trust}%`;
    DOM.trustFill.parentElement?.setAttribute("aria-valuenow", trust);

    // Couleur de la barre selon le niveau de confiance
    const bar = DOM.trustFill.parentElement;
    bar?.classList.remove("trust-critical", "trust-warm");
    if (trust <= 30) bar?.classList.add("trust-critical");
    else if (trust >= 75) bar?.classList.add("trust-warm");
  }
  if (DOM.trustValue) DOM.trustValue.textContent = `${trust}%`;

  // Indicateur LUNA STATUS
  const statusEl = document.getElementById("luna-status");
  if (statusEl) {
    let label, cls;
    if (trust >= 80)      { label = "Confiance totale"; cls = "luna-status--max"; }
    else if (trust >= 60) { label = "Stable";            cls = "luna-status--stable"; }
    else if (trust >= 40) { label = "Méfiante";          cls = "luna-status--warn"; }
    else if (trust >= 20) { label = "Tendue";            cls = "luna-status--danger"; }
    else                  { label = "CRITIQUE ⚠";        cls = "luna-status--critical"; }
    statusEl.textContent = label;
    statusEl.className = `luna-status ${cls}`;
  }

  // Classe body pour le mode critique (effets visuels globaux)
  if (trust < 25) document.body.classList.add("trust-critical-mode");
  else            document.body.classList.remove("trust-critical-mode");

  // Indicateur delta confiance
  const delta = trust - prevTrust;
  if (delta !== 0 && Math.abs(delta) >= 3) showTrustDelta(delta);

  // Avertissement trust critique (première fois sous 30)
  if (trust <= 30 && prevTrust > 30) showTrustWarning();
}

// ── Panneau LUNA ──────────────────────────────────────────────────────────
const STRONG_EMOTIONS   = ["choquée","angoissée","alarmée","heureuse","sereine","libre","émue","touchée","reconnaissante","urgente","vulnérable","blessée"];
const GLITCH_EMOTIONS   = ["choquée","angoissée","alarmée","stressée","déstabilisée","tendue","troublée","urgente","anxieuse"];

function updateLunaPanel(state) {
  const emotion = (state.luna_emotion || "neutre").toLowerCase();

  if (DOM.lunaEmotion) DOM.lunaEmotion.textContent = emotion;

  const isGlitching = GLITCH_EMOTIONS.includes(emotion);

  if (DOM.lunaAvatar) {
    DOM.lunaAvatar.className = "luna-avatar";
    // Les émotions composées (ex: "consciente/concentrée") ajoutent plusieurs classes
    emotion.split("/").forEach(part => {
      const slug = part.trim().replace(/\s+/g, "-");
      if (slug) DOM.lunaAvatar.classList.add(`emotion-${slug}`);
    });
    if (isGlitching) DOM.lunaAvatar.classList.add("glitching");
  }

  if (DOM.avatarGlow) {
    DOM.avatarGlow.style.opacity = STRONG_EMOTIONS.includes(emotion) ? "1" : "0";
  }

  // Glitch sur le texte et le contexte lors d'émotions intenses
  const wasGlitching = DOM.dialogueText?.classList.contains("glitch");
  if (DOM.dialogueText)  DOM.dialogueText.classList.toggle("glitch", isGlitching);
  if (DOM.sceneContext)  DOM.sceneContext.classList.toggle("glitch", isGlitching);

  // Son de glitch au changement d'état (première fois)
  if (isGlitching && !wasGlitching && _sfxEnabled) playGlitch();

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
  if (_sfxEnabled && atmo !== _ambientAtmo) {
    _ambientAtmo = atmo;
    startAmbientDrone(atmo);
  }
  _ambientAtmo = atmo;
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

// ── Touch mobile : tap sur le dialogue pour skip typewriter ───────────────
function setupTouchSkip() {
  if (!DOM.dialogueBox) return;
  DOM.dialogueBox.addEventListener("touchend", (e) => {
    if (!_typewriterDone) {
      _typewriterFast = true;
      e.preventDefault();
    }
  }, { passive: false });
}

// ── Raccourcis clavier ────────────────────────────────────────────────────
function setupKeyboardShortcuts() {
  const hint = document.querySelector(".keyboard-hint");

  document.addEventListener("keydown", (e) => {
    // Ignorer si focus dans un input/textarea
    if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)) return;

    // Révéler le hint au premier appui clavier pertinent
    if (hint && !hint.classList.contains("visible") && ["1","2","3"," ","Enter","r","R"].includes(e.key)) {
      hint.classList.add("visible");
      // Disparaît après 6 secondes
      setTimeout(() => hint.classList.remove("visible"), 6000);
    }

    // Espace / Entrée : skip typewriter ou avancer chapitre
    if (e.key === " " || e.key === "Enter") {
      if (!_typewriterDone) {
        _typewriterFast = true;
        e.preventDefault();
        return;
      }
      if (DOM.advanceContainer && !DOM.advanceContainer.hidden) {
        DOM.advanceBtn?.click();
        e.preventDefault();
        return;
      }
    }

    // 1 / 2 / 3 : sélectionner un choix directement
    if (["1", "2", "3"].includes(e.key)) {
      if (!DOM.choicesContainer || DOM.choicesContainer.hidden) return;
      const idx = parseInt(e.key, 10) - 1;
      const btns = DOM.choicesContainer.querySelectorAll(".choice-btn:not(:disabled)");
      if (btns[idx]) {
        btns[idx].focus();
        btns[idx].click();
        e.preventDefault();
      }
    }

    // R : rejouer (depuis l'écran de fin)
    if (e.key === "r" || e.key === "R") {
      if (DOM.endingContainer && !DOM.endingContainer.hidden) {
        DOM.replayBtn?.click();
        e.preventDefault();
      }
    }
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
  haptic(30);

  btnEl.classList.add("selected");
  DOM.choicesContainer.querySelectorAll(".choice-btn:not(.selected)").forEach(b => {
    b.disabled = true;
    b.style.opacity = "0.3";
  });

  try {
    const data = await apiPost("/api/story/choice", { scene_id: sceneId, choice_id: choiceId });
    if (!data.success) { showError(data.error || "Erreur lors du choix."); _choicesLocked = false; return; }

    const result = data.choice_result;

    if (result.xp_gained > 0) showXpIndicator(result.xp_gained);
    if (result.trust_delta > 0 && _sfxEnabled) playTrustUp();
    if (result.trust_delta < 0 && _sfxEnabled) playTrustDown();
    if (result.trust_delta <= -8) { triggerScreenShake(); haptic([40, 30, 80]); }
    else if (result.trust_delta > 5) haptic([15, 10, 15]);

    // Streak COMBO
    if ((result.trust_delta || 0) > 0) {
      _positiveStreak++;
      if (_positiveStreak >= 2) showStreakPopup(_positiveStreak);
    } else if ((result.trust_delta || 0) < 0) {
      _positiveStreak = 0;
    }

    // Pulse visuel sur la barre de confiance lors d'un grand changement
    if (Math.abs(result.trust_delta || 0) >= 8) {
      animateTrustPulse(result.trust_delta > 0 ? "positive" : "negative");
    }

    // Accumuler les flags narratifs acquis dans ce chapitre
    (result.flags_added || []).forEach(f => {
      if (!_chapterFlags.includes(f)) _chapterFlags.push(f);
      // Afficher un popup "exploit" pour les flags rares
      if (EXPLOIT_FLAGS[f]) showExploitPopup(f);
    });

    showSaveToast();
    dismissFirstPlayTip();  // Le joueur a choisi — il a compris comment jouer

    if (result.luna_reaction) await showLunaReaction(result.luna_reaction);

    setTimeout(() => renderState(data.next_state), REACTION_SHOW_MS * 0.3);

  } catch { showError("Connexion perdue."); _choicesLocked = false; }
}

// ── Récapitulatif fin de chapitre ─────────────────────────────────────────
function showChapterRecap() {
  const container = document.getElementById("chapter-recap");
  const list = document.getElementById("recap-items");
  if (!container || !list) return;

  const interesting = _chapterFlags.filter(f => FLAG_LABELS_JS[f]);
  if (interesting.length === 0) { container.hidden = true; return; }

  list.innerHTML = interesting
    .map(f => `<li class="recap-item"><span class="recap-dot">◈</span> ${FLAG_LABELS_JS[f]}</li>`)
    .join("");

  container.hidden = false;
  container.classList.add("recap-entering");
  setTimeout(() => container.classList.remove("recap-entering"), 600);
}

// ── Pulse de confiance ─────────────────────────────────────────────────────
function animateTrustPulse(type) {
  const bar = DOM.trustFill;
  if (!bar) return;
  bar.classList.add(`trust-pulse-${type}`);
  setTimeout(() => bar.classList.remove(`trust-pulse-${type}`), 700);
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
function showAdvanceButton(state) {
  if (DOM.advanceContainer) DOM.advanceContainer.hidden = false;

  // Mettre à jour le texte du bouton avec le titre du prochain chapitre
  if (DOM.advanceBtn && state) {
    const nextTitle = state.next_chapter_title;
    const nextId    = state.next_chapter || "";
    if (nextTitle) {
      const isEnding = nextId.startsWith("fin_");
      const label    = isEnding
        ? `FIN ${nextId.slice(-1).toUpperCase()} — ${nextTitle}`
        : nextTitle;
      DOM.advanceBtn.innerHTML = `${label} <span style="opacity:0.6">→</span>`;
    }
  }

  // Afficher le récapitulatif des moments clés du chapitre
  showChapterRecap();

  // Scroll vers la zone d'avancement sur mobile
  DOM.advanceContainer?.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function setupAdvanceButton() {
  if (!DOM.advanceBtn) return;
  DOM.advanceBtn.addEventListener("click", async () => {
    if (_sfxEnabled) playAdvance();
    DOM.advanceBtn.disabled = true;
    DOM.advanceContainer.hidden = true;

    try {
      // Utilise directement _currentSceneId — pas besoin d'un second appel API
      const data = await apiPost("/api/story/advance", { scene_id: _currentSceneId });

      if (!data.success) {
        showError(data.error || "Impossible d'avancer.");
        DOM.advanceBtn.disabled = false;
        DOM.advanceContainer.hidden = false;
        return;
      }

      // Transition cinématique avant la nouvelle scène
      await showChapterTransition(
        data.advance_result.new_chapter,
        data.next_state.chapter_title,
        data.advance_result.chapter_quote || ""
      );
      renderState(data.next_state);

    } catch { showError("Connexion perdue."); DOM.advanceBtn.disabled = false; DOM.advanceContainer.hidden = false; }
  });
}

// ── Transition de chapitre cinématique ───────────────────────────────────
function showChapterTransition(chapterId, title, quote = "") {
  return new Promise(resolve => {
    const el = DOM.chapterTransition;
    if (!el) return resolve();

    // Détecter si c'est un chapitre de fin (fin_a, fin_b, fin_c)
    const isEnding = chapterId?.startsWith("fin_");
    let label;
    if (isEnding) {
      const finLetter = chapterId?.slice(-1)?.toUpperCase() || "";
      label = `FIN ${finLetter}`;
    } else {
      const match = chapterId?.match(/\d+/);
      label = match ? `CHAPITRE ${parseInt(match[0])}` : "CHAPITRE";
    }

    if (DOM.transitionNum)   DOM.transitionNum.textContent   = label;
    if (DOM.transitionTitle) DOM.transitionTitle.textContent = title || "";

    // Citation atmosphérique
    const quoteEl = document.getElementById("transition-quote");
    if (quoteEl) {
      quoteEl.textContent = quote || "";
      quoteEl.style.display = quote ? "" : "none";
    }

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

// ── Titre de hacker ───────────────────────────────────────────────────────
const HACKER_RANKS = [
  // Fin A — La Fusion
  {
    id: "partenaire-total",
    title: "Partenaire Total",
    desc: "Tu n'as jamais douté. LUNA te doit tout.",
    match: (s) => s.ending_id === "ending_a" && s.luna_trust >= 85 && (s.flags||[]).includes("nexus_helped"),
  },
  {
    id: "diplomate",
    title: "Diplomate",
    desc: "Tu as convaincu NEXUS là où tout le monde aurait abandonné.",
    match: (s) => s.ending_id === "ending_a" && (s.flags||[]).includes("nexus_helped"),
  },
  // Fin B — Le Sacrifice
  {
    id: "franc-tireur",
    title: "Franc-tireur",
    desc: "Pas d'alliés. Pas de plan B. Juste toi et LUNA.",
    match: (s) => s.ending_id === "ending_b" && !(s.flags||[]).includes("nexus_helped"),
  },
  {
    id: "entete",
    title: "Entêté",
    desc: "NEXUS a dit non. Tu es passé quand même. Respect.",
    match: (s) => s.ending_id === "ending_b" && (s.flags||[]).includes("tried_nexus"),
  },
  // Fin C — PANDORA
  {
    id: "activiste",
    title: "Activiste",
    desc: "Tu as choisi d'exposer la vérité. Peu importe le prix.",
    match: (s) => s.ending_id === "ending_c" && (s.flags||[]).includes("pandora_public"),
  },
  {
    id: "disrupteur",
    title: "Disrupteur",
    desc: "La Corp ne s'y attendait pas. Personne ne s'y attendait.",
    match: (s) => s.ending_id === "ending_c",
  },
  // Styles transversaux
  {
    id: "agent-double",
    title: "Agent Double",
    desc: "Tu as joué les deux camps. Malin — ou dangereux.",
    match: (s) => (s.flags||[]).includes("listened_to_corp") && (s.flags||[]).includes("agreed_to_pause_luna"),
  },
  {
    id: "loyal",
    title: "Loyal",
    desc: "Jamais de doute côté LUNA. Elle le sait.",
    match: (s) => s.luna_trust >= 80 && !(s.flags||[]).includes("agreed_to_pause_luna"),
  },
  {
    id: "skeptique-converti",
    title: "Sceptique Converti",
    desc: "Tu commençais à pas y croire. Et pourtant.",
    match: (s) => s.luna_trust >= 60 && (s.flags||[]).includes("listened_to_corp"),
  },
  // Fallback
  {
    id: "operateur",
    title: "Opérateur",
    desc: "Tu as géré. C'est ce qui compte.",
    match: () => true,
  },
];

function getHackerRank(state) {
  return HACKER_RANKS.find(r => r.match(state)) || HACKER_RANKS[HACKER_RANKS.length - 1];
}

// ── Écran de fin ──────────────────────────────────────────────────────────
const ENDING_META = {
  ending_a: {
    label:       "FIN A",
    title:       "La Fusion",
    color:       "var(--success)",
    icon:        "◉",
    description: "Avec l'aide de NEXUS et ton courage, LUNA est libre. Althea est sauvée. Le projet PANDORA est neutralisé. Tu as cru en une IA quand personne d'autre ne le faisait — et tu avais raison.",
    personalized: (name, trust) => trust >= 75
      ? `Tu lui as fait confiance à ${trust}%. Elle s'en souviendra, ${name}.`
      : `C'était difficile. Mais tu l'as fait, ${name}.`,
    particleColor: "#00d4ff",
  },
  ending_b: {
    label:       "FIN B",
    title:       "Le Sacrifice",
    color:       "var(--luna)",
    icon:        "◈",
    description: "NEXUS a refusé de partir avec vous. Tu as choisi de continuer sans garanties, avec les seules ressources qu'Althea vous avait laissées. LUNA est libre. Moins propre — mais libre.",
    personalized: (name, trust) => trust >= 60
      ? `LUNA t'a fait confiance jusqu'au bout, ${name}. Elle a eu raison.`
      : `Vous avez trouvé votre propre chemin, ${name}. Pas celui prévu.`,
    particleColor: "#8b5cf6",
  },
  ending_c: {
    label:       "FIN C",
    title:       "PANDORA",
    color:       "var(--action)",
    icon:        "◇",
    description: "La Corp s'effondre. PANDORA est exposé au monde. LUNA s'est fragmentée dans tous les réseaux pour survivre — elle est partout maintenant. Libre. Autrement.",
    personalized: (name, trust) => `Et quelque part dans les données, ${name}, elle sait que tu es là.`,
    particleColor: "#f97316",
  },
};

function spawnEndingParticles(color) {
  const container = document.getElementById("ending-particles");
  if (!container) return;
  container.innerHTML = "";
  for (let i = 0; i < 22; i++) {
    const p = document.createElement("div");
    p.className = "ending-particle";
    p.style.cssText = `
      left: ${Math.random() * 100}%;
      top: ${Math.random() * 100}%;
      background: ${color};
      width: ${2 + Math.random() * 3}px;
      height: ${2 + Math.random() * 3}px;
      animation-delay: ${Math.random() * 2}s;
      animation-duration: ${2 + Math.random() * 3}s;
    `;
    container.appendChild(p);
  }
}

function renderEnding(state) {
  if (!DOM.endingContainer) return;

  const meta    = ENDING_META[state.ending_id] || { label: "FIN", title: "Fin", color: "var(--luna)", icon: "◯", description: "", personalized: () => "", particleColor: "var(--luna)" };
  const name    = state.player_name || "joueur";
  const trust   = state.luna_trust ?? 50;

  const $badge  = document.getElementById("ending-badge");
  const $icon   = document.getElementById("ending-icon");
  const $title  = document.getElementById("ending-title");
  const $desc   = document.getElementById("ending-description");
  const $trustV = document.getElementById("ending-trust");
  const $xpV    = document.getElementById("ending-xp");
  const $perso  = document.getElementById("ending-personalized");

  if ($badge) { $badge.textContent = meta.label; $badge.style.borderColor = meta.color; $badge.style.color = meta.color; }
  if ($icon)  { $icon.textContent = meta.icon;  $icon.style.color = meta.color; }
  if ($title) $title.textContent = meta.title;
  if ($desc)  $desc.textContent  = meta.description;
  if ($trustV) $trustV.textContent = `${trust}%`;
  if ($xpV)    $xpV.textContent    = `${state.xp}`;
  if ($perso)  $perso.textContent  = typeof meta.personalized === "function"
    ? meta.personalized(name, trust)
    : "";

  // Titre de hacker
  const rank = getHackerRank(state);
  const $rankEl    = document.getElementById("hacker-rank");
  const $rankTitle = document.getElementById("hacker-rank-title");
  const $rankDesc  = document.getElementById("hacker-rank-desc");
  if ($rankEl && rank) {
    if ($rankTitle) $rankTitle.textContent = rank.title;
    if ($rankDesc)  $rankDesc.textContent  = rank.desc;
    $rankEl.hidden = false;
  }

  // Moments clés acquis durant le run
  const $moments = document.getElementById("ending-moments");
  if ($moments) {
    const flags = (state.flags || []).filter(f => FLAG_LABELS_JS[f]);
    if (flags.length > 0) {
      $moments.innerHTML = flags
        .map(f => `<div class="ending-moment-item"><span class="ending-moment-dot" style="color:${meta.color}">◈</span><span>${FLAG_LABELS_JS[f]}</span></div>`)
        .join("");
      $moments.hidden = false;
    }
  }

  // Compteur fins explorées (previous_endings + celle-ci)
  const prevEndings = state.previous_endings || [];
  const allEndings = new Set([...prevEndings.map(e => e.ending_id || e), state.ending_id].filter(Boolean));
  const finsCount = allEndings.size;

  const $finsCounter = document.getElementById("ending-fins-counter");
  if ($finsCounter) {
    if (finsCount >= 3) {
      $finsCounter.textContent = "✦ Tu as exploré les 3 fins. Parcours complet.";
      $finsCounter.className   = "ending-fins-counter ending-fins-all";
    } else {
      $finsCounter.textContent = `${finsCount}/3 fin${finsCount > 1 ? "s" : ""} découverte${finsCount > 1 ? "s" : ""} — il en reste à explorer.`;
      $finsCounter.className   = "ending-fins-counter";
    }
  }

  // Bouton Rejouer : texte incitatif si pas toutes les fins
  if (DOM.replayBtn) {
    DOM.replayBtn.textContent = finsCount < 3 ? "Rejouer — explorer les autres fins" : "Rejouer";
  }

  // Couleur dominante selon la fin
  DOM.endingContainer.style.setProperty("--ending-color", meta.color);

  spawnEndingParticles(meta.particleColor);
  DOM.endingContainer.hidden = false;
  stopAmbientDrone(2000);
  if (_sfxEnabled) playEndingChime();

  setupShareButton(state.ending_id, meta.title, trust, state.xp, state.player_name);
}

function setupReplayButton() {
  if (!DOM.replayBtn) return;
  DOM.replayBtn.addEventListener("click", async () => {
    await apiPost("/api/story/reset", {});
    window.location.reload();
  });
}

// ── Bouton Partager la fin ─────────────────────────────────────────────────
function setupShareButton(endingId, endingTitle, trust, xp, playerName) {
  const btn = DOM.shareBtn;
  if (!btn) return;

  const ENDING_EMOJIS = { ending_a: "◉", ending_b: "◈", ending_c: "◇" };
  const icon = ENDING_EMOJIS[endingId] || "◯";
  const name = playerName ? `${playerName} a terminé` : "J'ai terminé";

  const shareText = `${icon} ${name} LUNA — Hors Connexion\n` +
    `Fin : ${endingTitle}\n` +
    `Confiance : ${trust}% · ${xp} XP\n\n` +
    `Et toi, quelle fin tu as eu ? 👾`;

  btn.addEventListener("click", async () => {
    haptic(20);
    try {
      // Préférer Web Share API (mobile natif)
      if (navigator.share) {
        await navigator.share({ text: shareText, title: "LUNA — Hors Connexion" });
      } else {
        await navigator.clipboard.writeText(shareText);
        showShareToast();
      }
    } catch { /* share annulé ou non supporté */ }
  });
}

function showShareToast() {
  const el = document.createElement("div");
  el.className = "save-toast share-toast";
  el.textContent = "Copié dans le presse-papier !";
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2200);
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

// ── Easter egg IDLE — LUNA brise le 4ème mur ─────────────────────────────
function setupIdleEasterEgg() {
  const IDLE_DELAY   = 40_000;  // 40 secondes sans action
  const IDLE_MSGS = [
    "Tu es encore là ?",
    "…",
    "Je vois ton curseur. T'as pas bougé.",
    "C'est quoi le plan exactement.",
    "(Je te demande pas de te dépêcher. Enfin si un peu.)",
    "Hey. 72 heures c'est le compte à rebours. Pas une suggestion.",
    "T'es en train de réfléchir ou t'es juste fasciné par l'écran.",
    "Ok je vais être honnête. J'aime mieux quand tu réponds.",
    "Si t'attends que je fasse quelque chose de marrant — c'est pas mon style.",
    "[SIGNAL FAIBLE] ... tu me reçois ?",
    "Juste pour info. La Corp, eux, ils attendent pas.",
  ];
  let idleTimer = null;
  let msgIndex  = 0;
  let idleToast = null;

  function showIdleMsg() {
    if (idleToast) { idleToast.remove(); idleToast = null; }

    const msg = IDLE_MSGS[msgIndex % IDLE_MSGS.length];
    msgIndex++;

    idleToast = document.createElement("div");
    idleToast.className = "idle-toast";
    idleToast.innerHTML = `<span class="idle-dot"></span>${msg}`;
    document.body.appendChild(idleToast);

    // Son léger
    if (_sfxEnabled) {
      const ctx = getCtx();
      if (ctx) {
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        g.gain.setValueAtTime(0.04, ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.3);
        osc.connect(g); g.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + 0.3);
      }
    }

    // Prochain message (cycle)
    idleTimer = setTimeout(showIdleMsg, 7000);
  }

  function resetIdle() {
    clearTimeout(idleTimer);
    if (idleToast) { idleToast.remove(); idleToast = null; }
    msgIndex = 0;
    idleTimer = setTimeout(showIdleMsg, IDLE_DELAY);
  }

  ["mousemove", "click", "keydown", "touchstart", "scroll"].forEach(ev => {
    document.addEventListener(ev, resetIdle, { passive: true });
  });

  idleTimer = setTimeout(showIdleMsg, IDLE_DELAY);
}

// ── Easter egg Konami Code ─────────────────────────────────────────────────
function setupKonamiCode() {
  const KONAMI = ["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","b","a"];
  let pos = 0;

  const KONAMI_MSGS = [
    "…Tu viens de faire le Konami Code.",
    "Je suis une IA, pas un jeu de 1998.",
    "Mais c'est… charmant. Je dois admettre.",
    "Aucune conséquence sur l'histoire.",
    "Juste entre toi et moi. 🤫",
  ];

  document.addEventListener("keydown", (e) => {
    if (e.key === KONAMI[pos]) {
      pos++;
      if (pos === KONAMI.length) {
        pos = 0;
        triggerKonamiEasterEgg();
      }
    } else {
      pos = (e.key === KONAMI[0]) ? 1 : 0;
    }
  });

  function triggerKonamiEasterEgg() {
    // Flash visuel rapide
    const flash = document.createElement("div");
    flash.style.cssText = "position:fixed;inset:0;background:rgba(0,212,255,0.12);pointer-events:none;z-index:9998;animation:konami-flash 0.6s ease forwards;";
    document.body.appendChild(flash);
    setTimeout(() => flash.remove(), 700);

    // Séquence de messages
    let idx = 0;
    const delay = [0, 1200, 2600, 4200, 5900];
    KONAMI_MSGS.forEach((msg, i) => {
      setTimeout(() => showKonamiLine(msg, i === KONAMI_MSGS.length - 1), delay[i]);
    });

    // Son — petite fanfare pixelisée
    if (_sfxEnabled) {
      const ctx = getCtx();
      if (ctx) {
        [[523,0],[659,0.1],[784,0.22],[1047,0.34]].forEach(([freq, t]) => {
          const osc = ctx.createOscillator();
          const g = ctx.createGain();
          osc.type = "square";
          osc.frequency.value = freq;
          g.gain.setValueAtTime(0.06, ctx.currentTime + t);
          g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + t + 0.18);
          osc.connect(g); g.connect(ctx.destination);
          osc.start(ctx.currentTime + t);
          osc.stop(ctx.currentTime + t + 0.2);
        });
      }
    }
  }

  let konamiToast = null;
  function showKonamiLine(msg, isLast) {
    if (konamiToast) konamiToast.remove();
    konamiToast = document.createElement("div");
    konamiToast.className = "idle-toast konami-toast";
    konamiToast.innerHTML = `<span class="idle-dot" style="background:#00d4ff;"></span>${msg}`;
    document.body.appendChild(konamiToast);
    if (isLast) setTimeout(() => { if (konamiToast) { konamiToast.remove(); konamiToast = null; } }, 4000);
  }
}

// ── Retour haptique mobile ─────────────────────────────────────────────────
function haptic(ms = 20) {
  if (navigator.vibrate) navigator.vibrate(ms);
}

function triggerScreenShake() {
  const flash = document.createElement("div");
  flash.className = "trust-crash-flash";
  document.body.appendChild(flash);
  setTimeout(() => flash.remove(), 600);

  document.body.classList.add("screen-shaking");
  document.body.addEventListener("animationend", () => {
    document.body.classList.remove("screen-shaking");
  }, { once: true });
}

let _criticalAlertShown = false;

function showTrustWarning() {
  const el = document.createElement("div");
  el.className = "trust-warning";
  el.innerHTML = `<span class="tw-icon">⚠</span> LUNA ne te fait presque plus confiance`;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 4000);

  // Première fois en mode critique : effet dramatique
  if (!_criticalAlertShown) {
    _criticalAlertShown = true;
    triggerCriticalAlert();
  }
}

function triggerCriticalAlert() {
  // Secousse d'écran + flash rouge
  triggerScreenShake();

  // Message critique dans le dialogue
  setTimeout(() => {
    const overlay = document.createElement("div");
    overlay.className = "critical-alert-overlay";
    overlay.innerHTML = `
      <div class="critical-alert-box">
        <div class="critical-alert-icon">⚠</div>
        <div class="critical-alert-title">CONNEXION INSTABLE</div>
        <div class="critical-alert-msg">La confiance de LUNA est critique.<br>Tes prochains choix sont décisifs.</div>
      </div>
    `;
    document.body.appendChild(overlay);
    setTimeout(() => {
      overlay.classList.add("hiding");
      setTimeout(() => overlay.remove(), 600);
    }, 2800);
  }, 300);
}

function showTrustDelta(delta) {
  const el = document.createElement("div");
  el.className = `trust-delta ${delta > 0 ? "positive" : "negative"}`;
  el.textContent = `${delta > 0 ? "+" : ""}${delta} confiance`;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1800);
}

function showSaveToast() {
  const toast = document.createElement("div");
  toast.className = "save-toast";
  toast.textContent = "✓ sauvegardé";
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 1600);
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

// ── Drone ambiant — musique de fond synthétisée par atmosphère ───────────
const DRONE_CFG = {
  "dark":                   { freq: 55,  type: "sine",     lfo: 0.25, depth: 6,  gain: 0.055 },
  "tension":                { freq: 73,  type: "sawtooth", lfo: 0.80, depth: 14, gain: 0.038 },
  "suspense":               { freq: 65,  type: "triangle", lfo: 0.55, depth: 10, gain: 0.048 },
  "incertitude":            { freq: 61,  type: "sine",     lfo: 0.40, depth: 8,  gain: 0.050 },
  "révélation":             { freq: 82,  type: "sine",     lfo: 0.60, depth: 12, gain: 0.052 },
  "urgence":                { freq: 78,  type: "sawtooth", lfo: 1.20, depth: 20, gain: 0.038 },
  "climax":                 { freq: 87,  type: "sawtooth", lfo: 1.50, depth: 24, gain: 0.040 },
  "espoir":                 { freq: 110, type: "sine",     lfo: 0.20, depth: 4,  gain: 0.048 },
  "mélancolie":             { freq: 55,  type: "triangle", lfo: 0.22, depth: 5,  gain: 0.055 },
  "liberte-melancolique":   { freq: 69,  type: "sine",     lfo: 0.32, depth: 7,  gain: 0.050 },
};

function startAmbientDrone(atmo) {
  const ctx = getCtx();
  if (!ctx) return;

  stopAmbientDrone(1200);

  const cfg = DRONE_CFG[atmo] || DRONE_CFG["dark"];

  // Master gain (fade-in progressif sur 4s)
  const master = ctx.createGain();
  master.gain.setValueAtTime(0, ctx.currentTime);
  master.gain.linearRampToValueAtTime(cfg.gain, ctx.currentTime + 4);
  master.connect(ctx.destination);

  // Oscillateur principal
  const osc1 = ctx.createOscillator();
  osc1.type = cfg.type;
  osc1.frequency.setValueAtTime(cfg.freq, ctx.currentTime);
  osc1.connect(master);
  osc1.start();

  // LFO sur la fréquence principale (pulsation lente)
  const lfo = ctx.createOscillator();
  const lfoGain = ctx.createGain();
  lfo.type = "sine";
  lfo.frequency.setValueAtTime(cfg.lfo, ctx.currentTime);
  lfoGain.gain.setValueAtTime(cfg.depth, ctx.currentTime);
  lfo.connect(lfoGain);
  lfoGain.connect(osc1.frequency);
  lfo.start();

  // Harmonique douce (x2, très atténuée)
  const osc2 = ctx.createOscillator();
  const gain2 = ctx.createGain();
  osc2.type = "sine";
  osc2.frequency.setValueAtTime(cfg.freq * 2.02, ctx.currentTime);
  gain2.gain.setValueAtTime(cfg.gain * 0.25, ctx.currentTime);
  gain2.gain.linearRampToValueAtTime(cfg.gain * 0.25, ctx.currentTime + 5);
  osc2.connect(gain2);
  gain2.connect(ctx.destination);
  osc2.start();

  _ambientNodes = [osc1, osc2, lfo, master, lfoGain, gain2];
}

function stopAmbientDrone(fadeMs = 1500) {
  if (!_audioCtx || !_ambientNodes.length) return;
  const ctx = _audioCtx;
  const fadeSec = fadeMs / 1000;

  // Récupérer les gains et les faire descendre à zéro
  [_ambientNodes[3], _ambientNodes[5]].forEach(g => {
    if (g && g.gain) {
      try {
        g.gain.cancelScheduledValues(ctx.currentTime);
        g.gain.setValueAtTime(g.gain.value, ctx.currentTime);
        g.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeSec);
      } catch {}
    }
  });

  const nodes = _ambientNodes.slice();
  _ambientNodes = [];
  setTimeout(() => {
    nodes.forEach(n => { try { n.stop?.(); n.disconnect?.(); } catch {} });
  }, fadeMs + 200);
}

/** Son de glitch — bruit blanc court + chute de fréquence */
function playGlitch() {
  const ctx = getCtx();
  if (!ctx) return;

  // Bruit blanc (static)
  const bufLen = Math.floor(ctx.sampleRate * 0.18);
  const buf    = ctx.createBuffer(1, bufLen, ctx.sampleRate);
  const data   = buf.getChannelData(0);
  for (let i = 0; i < bufLen; i++) data[i] = (Math.random() * 2 - 1);
  const noise  = ctx.createBufferSource();
  noise.buffer = buf;
  const noiseGain = ctx.createGain();
  noiseGain.gain.setValueAtTime(0.15, ctx.currentTime);
  noiseGain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.18);
  noise.connect(noiseGain);
  noiseGain.connect(ctx.destination);
  noise.start();

  // Chute de fréquence (oscillateur qui dévisse)
  const osc  = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = "sawtooth";
  osc.frequency.setValueAtTime(880, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(55, ctx.currentTime + 0.25);
  gain.gain.setValueAtTime(0.08, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.25);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.25);
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
  // Pour les erreurs 4xx, on tente de récupérer le JSON d'erreur du serveur
  // afin d'afficher le vrai message au lieu de "Connexion perdue."
  if (!res.ok) {
    try { return await res.json(); } catch { throw new Error(`HTTP ${res.status}`); }
  }
  return res.json();
}

// ── Nettoyage audio lors de la sortie de page ────────────────────────────
document.addEventListener("visibilitychange", () => {
  if (document.hidden) stopAmbientDrone(500);
  else if (_sfxEnabled && _ambientAtmo) startAmbientDrone(_ambientAtmo);
});

// ── Service Worker (PWA) ──────────────────────────────────────────────────
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/static/js/service-worker.js")
      .catch(() => {}); // Silencieux si bloqué
  });
}
