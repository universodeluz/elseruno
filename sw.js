// Service Worker — El Ser Uno
// Sube este archivo a la RAÍZ del repositorio (mismo nivel que index.html)

const CACHE_VERSION = 'el-ser-uno-v1'; // Sube este número cada vez que publiques cambios importantes
const OFFLINE_URL = '/elseruno/index.html';

// Archivos que se guardan de inmediato al instalar (ajusta a tu estructura real)
const PRECACHE_ASSETS = [
  '/elseruno/index.html',
  '/elseruno/manifest.json'
];

// --- Instalación: precachea lo esencial ---
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => cache.addAll(PRECACHE_ASSETS))
  );
  self.skipWaiting();
});

// --- Activación: limpia cachés viejos ---
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_VERSION)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// --- Fetch: estrategia "network first, fallback a caché" ---
// Así cada página HTML se actualiza cuando hay internet, pero sigue
// disponible offline si ya fue visitada una vez.
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const responseClone = response.clone();
        caches.open(CACHE_VERSION).then((cache) => {
          cache.put(event.request, responseClone);
        });
        return response;
      })
      .catch(() =>
        caches.match(event.request).then((cached) => {
          return cached || caches.match(OFFLINE_URL);
        })
      )
  );
});
