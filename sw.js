// Najpierw sieć, a bez sieci ostatnia zapisana wersja strony. Pliki audio i wideo pomijamy.
const C='nauka-v1';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin||/\.(mp3|m4a|mp4|epub|pdf)$/i.test(u.pathname))return;
  e.respondWith(fetch(r).then(res=>{
    if(res.ok){const k=res.clone();caches.open(C).then(c=>c.put(r,k));}
    return res;
  }).catch(()=>caches.match(r)));
});
