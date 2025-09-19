#!/usr/bin/env bash
set -e

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 'FAKETIME' [--gmt] command [args...]"
  exit 1
fi
FAKETIME_VAL="$1"
shift

FORCE_GMT=0
if [ "$1" = "--gmt" ]; then
  FORCE_GMT=1
  shift
fi

LIB=$(ldconfig -p 2>/dev/null | grep libfaketime | head -n1 | awk '{print $4}')
if [ -z "$LIB" ]; then
  for p in /usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1 /usr/lib/libfaketime.so.1 /usr/local/lib/libfaketime.so.1; do
    if [ -f "$p" ]; then
      LIB=$p
      break
    fi
  done
fi

if [ -z "$LIB" ]; then
  echo "libfaketime not found. Install it (Debian/Ubuntu: sudo apt install libfaketime)"
  exit 2
fi

ENVVARS=("LD_PRELOAD=$LIB" "FAKETIME=$FAKETIME_VAL")
if [ "$FORCE_GMT" -eq 1 ]; then
  ENVVARS+=("TZ=UTC")
fi

ENVSTR=""
for e in "${ENVVARS[@]}"; do
  ENVSTR+="$e "
done

exec env $ENVSTR "$@"
