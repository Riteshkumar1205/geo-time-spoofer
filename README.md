# geo-time-spoofer

Dev/test toolkit to emit fake GPS (NMEA) to a virtual PTY, run processes under a fake time, and override browser geolocation for consenting clients on your LAN.

Features:
- Python NMEA generator (writes to a PTY)
- libfaketime wrapper to run binaries with a faked clock
- Flask LAN UI to enter lat/lon/alt and optionally a Google Form URL
- Chrome extension (dev) to accept messages from the UI and inject `navigator.geolocation` into Chrome

**IMPORTANT:** Only use on machines/browsers you own or have explicit permission to test. Keep the secret token private. Do not use to deceive others or commit illegal acts.
