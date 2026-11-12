if ("serviceWorker" in navigator && location.protocol !== "file:") {
  const serviceWorkerUrl = new URL("../service-worker.js", document.currentScript.src);
  navigator.serviceWorker.register(serviceWorkerUrl).catch((error) => {
    console.error("Service worker registration failed:", error);
  });
}
