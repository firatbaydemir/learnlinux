if ("serviceWorker" in navigator && location.protocol !== "file:") {
  const serviceWorkerUrl = new URL("../service-worker.js", document.currentScript.src);
  // Eski worker varken yeni surum devralirsa sayfayi bir kez yenile (ilk ziyarette yenileme yok).
  const hadController = !!navigator.serviceWorker.controller;
  let reloaded = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (!hadController || reloaded) return;
    reloaded = true;
    location.reload();
  });
  navigator.serviceWorker.register(serviceWorkerUrl).catch((error) => {
    console.error("Service worker registration failed:", error);
  });
}
