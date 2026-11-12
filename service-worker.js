importScripts("./precache-manifest.js");

const CACHE_PREFIX = "temel-linux-akademisi-";
const CACHE_NAME = CACHE_PREFIX + self.PRECACHE_REVISION;

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    const urls = self.PRECACHE_URLS.map((path) => new URL(path, self.registration.scope).href);
    await cache.addAll(urls);
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names
      .filter((name) => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME)
      .map((name) => caches.delete(name)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin ||
      !url.href.startsWith(self.registration.scope)) {
    return;
  }

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    if (request.mode !== "navigate") {
      const cached = await cache.match(request);
      if (cached) return cached;
    }

    try {
      const response = await fetch(request);
      if (response.ok) await cache.put(request, response.clone());
      return response;
    } catch (error) {
      const cached = await cache.match(request, { ignoreSearch: true });
      if (cached) return cached;
      if (request.mode === "navigate") {
        const home = new URL("index.html", self.registration.scope);
        const fallback = await cache.match(home.href);
        if (fallback) return fallback;
      }
      throw error;
    }
  })());
});
