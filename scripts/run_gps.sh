#!/usr/bin/env bash
set -e
DEVICE=${1:-/tmp/virtualGPS_master}
LAT=${2:-28.4167}
LON=${3:-77.0488}
ALT=${4:-250}
RATE=1
FORCE_GMT=0

if [ "$5" = "--rate" ]; then
  RATE=$6
fi
if [ "$5" = "--gmt" ] || [ "$6" = "--gmt" ]; then
  FORCE_GMT=1
fi

if [ -f ./venv/bin/activate ]; then
  source ./venv/bin/activate
fi

CMD=(python3 nmea_generator.py --device "$DEVICE" --lat "$LAT" --lon "$LON" --alt "$ALT" --rate "$RATE")
if [ "$FORCE_GMT" -eq 1 ]; then
  CMD+=(--gmt)
fi

"${CMD[@]}"
