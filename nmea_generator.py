#!/usr/bin/env python3
"""
NMEA generator with high-precision formatting and optional GMT/UTC forcing.
Emits GGA + RMC sentences repeatedly to a serial device.
"""
import argparse
import serial
import time
from datetime import datetime, timezone
import os

def checksum(sentence: str) -> str:
    s = 0
    for ch in sentence:
        s ^= ord(ch)
    return format(s, '02X')

def format_lat(lat: float):
    hemi = 'N' if lat >= 0 else 'S'
    lat_abs = abs(lat)
    degrees = int(lat_abs)
    minutes = (lat_abs - degrees) * 60
    return f"{degrees:02d}{minutes:09.5f}", hemi

def format_lon(lon: float):
    hemi = 'E' if lon >= 0 else 'W'
    lon_abs = abs(lon)
    degrees = int(lon_abs)
    minutes = (lon_abs - degrees) * 60
    return f"{degrees:03d}{minutes:09.5f}", hemi

def make_gga(now: datetime, lat, lon, alt):
    time_str = now.strftime('%H%M%S')
    lat_f, lat_h = format_lat(lat)
    lon_f, lon_h = format_lon(lon)
    fields = [time_str, lat_f, lat_h, lon_f, lon_h, '1', '10', '0.8', f"{alt:.2f}", 'M', '', 'M', '', '']
    body = 'GPGGA,' + ','.join(fields)
    cs = checksum(body)
    return f"${body}*{cs}\r\n"

def make_rmc(now: datetime, lat, lon, speed_kn=0.0, track=0.0):
    time_str = now.strftime('%H%M%S')
    date_str = now.strftime('%d%m%y')
    lat_f, lat_h = format_lat(lat)
    lon_f, lon_h = format_lon(lon)
    fields = [time_str, 'A', lat_f, lat_h, lon_f, lon_h, f"{speed_kn:.1f}", f"{track:.1f}", date_str, '', '']
    body = 'GPRMC,' + ','.join(fields)
    cs = checksum(body)
    return f"${body}*{cs}\r\n"

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--device', required=True, help='serial device to write NMEA to')
    p.add_argument('--lat', type=float, required=True)
    p.add_argument('--lon', type=float, required=True)
    p.add_argument('--alt', type=float, default=0.0)
    p.add_argument('--rate', type=float, default=1.0, help='updates per second')
    p.add_argument('--gmt', action='store_true', help='force timestamps and TZ to GMT/UTC')
    args = p.parse_args()

    if args.gmt:
        os.environ['TZ'] = 'UTC'

    ser = serial.Serial(args.device, baudrate=4800, timeout=1)
    try:
        while True:
            now = datetime.now(timezone.utc)
            gga = make_gga(now, args.lat, args.lon, args.alt)
            rmc = make_rmc(now, args.lat, args.lon)
            ser.write(gga.encode('ascii'))
            ser.write(rmc.encode('ascii'))
            ser.flush()
            time.sleep(1.0 / args.rate)
    except KeyboardInterrupt:
        print('Stopping')
    finally:
        ser.close()

if __name__ == '__main__':
    main()
