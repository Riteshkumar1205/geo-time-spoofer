chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (!msg || msg.type !== 'INJECT') return;
  const lat = msg.lat;
  const lon = msg.lon;
  const alt = msg.alt || 0;
  const target = msg.url && msg.url.length ? msg.url : `https://www.google.com/maps/@${lat},${lon},18z`;
  chrome.tabs.create({url: target}, (tab) => {
    const code = `
      (function(){
        const lat=${lat}; const lon=${lon}; const alt=${alt};
        function makePos() { return { coords: { latitude: lat, longitude: lon, altitude: alt, accuracy: 1, altitudeAccuracy: 1, heading: null, speed: null }, timestamp: Date.now() }; }
        try{
          window.navigator.geolocation.getCurrentPosition = function(success, error){ try{ success(makePos()); } catch(e){ if(error) error(e); } };
          window.navigator.geolocation.watchPosition = function(success, error){ const id = setInterval(()=>{ try{ success(makePos()); } catch(e){ if(error) error(e); } },1000); return id; };
          window.navigator.geolocation.clearWatch = function(id){ clearInterval(id); };
        }catch(e){console.error('inject geolocation failed', e);}
      })();
    `;
    const listener = (tabId, changeInfo, t) => {
      if (tabId === tab.id && changeInfo.status === 'complete') {
        chrome.scripting.executeScript({ target: {tabId: tab.id}, func: new Function(code) })
          .catch((err)=>console.error('injection failed', err));
        chrome.tabs.onUpdated.removeListener(listener);
      }
    };
    chrome.tabs.onUpdated.addListener(listener);
  });
});
