self.addEventListener("install", event => {
  console.log("✅ Shiv ByajKhata Service Worker installing...");
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", event => {
  console.log("🚀 Shiv ByajKhata Service Worker activated!");
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.open("shiv-byajkhata-cache").then(cache => {
      return cache.match(event.request).then(response => {
        return (
          response ||
          fetch(event.request).then(networkResponse => {
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          })
        );
      });
    })
  );
});
