// Service Worker — LUNA Hors Connexion
const CACHE = "luna-v6";
const PRECACHE = [
  "/",
  "/game",
  "/profil",
  "/leaderboard",
  "/static/css/game.css",
  "/static/js/hacker-ranks.js",
  "/static/js/game.js",
  "/favicon.ico",
  "/static/manifest.json",
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(PRECACHE))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Stratégie : network-first pour l'API, cache-first pour les assets statiques
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);

  // API → toujours réseau, jamais cache
  if (url.pathname.startsWith("/api/")) return;

  // Assets statiques → cache-first
  if (url.pathname.startsWith("/static/")) {
    e.respondWith(
      caches.match(e.request).then((cached) =>
        cached || fetch(e.request).then((res) => {
          if (!res || !res.ok) return res;
          const clone = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
          return res;
        })
      )
    );
    return;
  }

  // Pages HTML → network-first, fallback cache
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        if (!res || !res.ok) return res;
        const clone = res.clone();
        caches.open(CACHE).then((c) => c.put(e.request, clone));
        return res;
      })
      .catch(() => caches.match(e.request).then((cached) => cached || caches.match("/")))
  );
});
