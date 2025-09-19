document.getElementById('apply').addEventListener('click', async () => {
  const lat = parseFloat(document.getElementById('lat').value);
  const lon = parseFloat(document.getElementById('lon').value);
  const alt = parseFloat(document.getElementById('alt').value) || 0;
  const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  if (!tab) return;
  chrome.scripting.executeScript({
    target: {tabId: tab.id},
    args: [lat, lon, alt],
    func: (lat, lon, alt) => {
      const script = document.createElement('script');
      script.textContent = `
        (function(){
          const lat=${lat}; const lon=${lon}; const alt=${alt};
          function makePos() { return { coords: { latitude: lat, longitude: lon, altitude: alt, accuracy: 1, altitudeAccuracy: 1, heading: null, speed: null }, timestamp: Date.now() }; }
          window.navigator.geolocation.getCurrentPosition = function(success, error){ try{ success(makePos()); } catch(e){ if(error) error(e); } };
          window.navigator.geolocation.watchPosition = function(success, error){ const id = setInterval(()=>{ try{ success(makePos()); } catch(e){ if(error) error(e); } },1000); return id; };
          window.navigator.geolocation.clearWatch = function(id){ clearInterval(id); };
        })();
      `;
      document.documentElement.appendChild(script);
      script.parentNode.removeChild(script);
    }
  });
  window.close();
});
