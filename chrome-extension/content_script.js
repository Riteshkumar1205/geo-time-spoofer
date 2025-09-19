const EXPECTED_TOKEN = 'REPLACE_WITH_TOKEN';

// Listen for page -> window.postMessage from the Flask UI
window.addEventListener('message', (event) => {
  if (event.source !== window) return;
  const d = event.data;
  if (!d || d.type !== 'INJECT_GEO') return;
  if (d.token !== EXPECTED_TOKEN) {
    console.warn('Rejecting INJECT_GEO with bad token');
    return;
  }
  // send to background with url so background opens the intended page
  chrome.runtime.sendMessage({type: 'INJECT', lat: d.lat, lon: d.lon, alt: d.alt, url: d.url || ''});
});
