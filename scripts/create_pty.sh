#!/usr/bin/env bash
set -e
if ! command -v socat >/dev/null 2>&1; then
  echo "socat is required. Install it: sudo apt install socat"
  exit 1
fi

socat -d -d PTY,raw,echo=0,link="/tmp/virtualGPS_slave" PTY,raw,echo=0,link="/tmp/virtualGPS_master" &
PID=$!
sleep 0.3

echo "Created virtual PTY pair:"
echo "  Slave (for apps/gpsd): /tmp/virtualGPS_slave"
echo "  Master (write NMEA to this): /tmp/virtualGPS_master"
echo "socat PID: $PID"
echo "To stop: kill $PID"
