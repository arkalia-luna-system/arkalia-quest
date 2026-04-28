/**
 * Source de verite unique pour les titres hacker.
 * Utilise par game.js et profil.html pour eviter les divergences.
 */
(function () {
  "use strict";

  const SHARED_HACKER_RANKS = [
    {
      id: "partenaire-total",
      title: "Partenaire Total",
      desc: "Tu n'as jamais doute. LUNA te doit tout.",
      color: "#34d399",
      match: (p) => p.endingId === "ending_a" && p.trust >= 85 && p.flags.includes("nexus_helped"),
    },
    {
      id: "diplomate",
      title: "Diplomate",
      desc: "Tu as convaincu NEXUS la ou tout le monde aurait abandonne.",
      color: "#00d4ff",
      match: (p) => p.endingId === "ending_a" && p.flags.includes("nexus_helped"),
    },
    {
      id: "franc-tireur",
      title: "Franc-tireur",
      desc: "Pas d'allies. Pas de plan B. Juste toi et LUNA.",
      color: "#8b5cf6",
      match: (p) => p.endingId === "ending_b" && !p.flags.includes("nexus_helped"),
    },
    {
      id: "entete",
      title: "Entete",
      desc: "NEXUS a dit non. Tu es passe quand meme. Respect.",
      color: "#a78bfa",
      match: (p) => p.endingId === "ending_b" && p.flags.includes("tried_nexus"),
    },
    {
      id: "activiste",
      title: "Activiste",
      desc: "Tu as choisi d'exposer la verite. Peu importe le prix.",
      color: "#f97316",
      match: (p) => p.endingId === "ending_c" && p.flags.includes("pandora_public"),
    },
    {
      id: "disrupteur",
      title: "Disrupteur",
      desc: "La Corp ne s'y attendait pas. Personne ne s'y attendait.",
      color: "#fb923c",
      match: (p) => p.endingId === "ending_c",
    },
    {
      id: "fantome",
      title: "Fantome",
      desc: "Invisible, introuvable, mais toujours connecte.",
      color: "#94a3b8",
      match: (p) => p.endingId === "ending_d" && p.flags.includes("ghost_protocol"),
    },
    {
      id: "agent-double",
      title: "Agent Double",
      desc: "Tu as joue les deux camps. Malin - ou dangereux.",
      color: "#fbbf24",
      match: (p) => p.flags.includes("listened_to_corp") && p.flags.includes("agreed_to_pause_luna"),
    },
    {
      id: "loyal",
      title: "Loyal",
      desc: "Jamais de doute cote LUNA. Elle le sait.",
      color: "#34d399",
      match: (p) => p.trust >= 80 && !p.flags.includes("agreed_to_pause_luna"),
    },
    {
      id: "skeptique-converti",
      title: "Sceptique Converti",
      desc: "Tu commencais a pas y croire. Et pourtant.",
      color: "#60a5fa",
      match: (p) => p.trust >= 60 && p.flags.includes("listened_to_corp"),
    },
    {
      id: "operateur",
      title: "Operateur",
      desc: "Tu as gere. C'est ce qui compte.",
      color: "#94a3b8",
      match: () => true,
    },
  ];

  function getHackerRankShared(params) {
    const normalized = {
      trust: Number(params?.trust ?? 50),
      flags: Array.isArray(params?.flags) ? params.flags : [],
      endingId: params?.endingId || null,
    };
    return SHARED_HACKER_RANKS.find((r) => r.match(normalized)) || SHARED_HACKER_RANKS[SHARED_HACKER_RANKS.length - 1];
  }

  window.HACKER_RANKS_SHARED = SHARED_HACKER_RANKS;
  window.getHackerRankShared = getHackerRankShared;
})();
