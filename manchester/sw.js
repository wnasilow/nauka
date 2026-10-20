// Fiszki Manchester: offline. Karty i lista odcinków najpierw z sieci, nagrania i powłoka z pamięci.
const C='mch-v2';
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(['./','index.html','manifest.webmanifest','icon-192.png'])));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin)return;
  const siec=/\/(karty|odcinki)\.json$|\/feed\.xml$|\/$|index\.html$/.test(u.pathname);
  if(siec){e.respondWith(fetch(e.request).then(r=>{const k=r.clone();caches.open(C).then(c=>c.put(e.request,k));return r}).catch(()=>caches.match(e.request)));return}
  e.respondWith(caches.match(e.request).then(m=>m||fetch(e.request).then(r=>{if(r.ok&&r.status===200){const k=r.clone();caches.open(C).then(c=>c.put(e.request,k))}return r})));
});
