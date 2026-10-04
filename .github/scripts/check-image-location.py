#!/usr/bin/env python3
# Fail if any image in the site carries GPS location data
# Phone photos record where they were taken, and Pages serves images byte for byte
# Usage: check-image-location.py [path ...]   (default: every image under the current directory)
import os
import re
import struct
import sys

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SKIP_DIRS = {".git", "_site", ".jekyll-cache", "vendor", "node_modules"}
GPS_IFD_TAG = 0x8825
XMP_GPS = re.compile(rb"GPS(Latitude|Longitude|Altitude)")


def exif_has_gps(tiff):
    # The GPS block hangs off the first IFD of the TIFF-structured EXIF data
    if len(tiff) < 8 or tiff[:2] not in (b"II", b"MM"):
        return False
    end = "<" if tiff[:2] == b"II" else ">"
    (offset,) = struct.unpack(end + "I", tiff[4:8])
    if offset + 2 > len(tiff):
        return False
    (count,) = struct.unpack(end + "H", tiff[offset:offset + 2])
    for i in range(count):
        entry = offset + 2 + i * 12
        if entry + 2 > len(tiff):
            break
        (tag,) = struct.unpack(end + "H", tiff[entry:entry + 2])
        if tag == GPS_IFD_TAG:
            return True
    return False


def jpeg_blocks(data):
    # APP1 holds both EXIF and XMP; stop at the start of scan
    i = 2
    while i + 4 <= len(data) and data[i] == 0xFF:
        marker = data[i + 1]
        if marker in (0xD9, 0xDA):
            break
        (length,) = struct.unpack(">H", data[i + 2:i + 4])
        payload = data[i + 4:i + 2 + length]
        if marker == 0xE1:
            if payload.startswith(b"Exif\0\0"):
                yield "exif", payload[6:]
            else:
                yield "xmp", payload
        i += 2 + length


def png_blocks(data):
    i = 8
    while i + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[i:i + 8])
        payload = data[i + 8:i + 8 + length]
        if kind == b"eXIf":
            yield "exif", payload
        elif kind in (b"iTXt", b"tEXt", b"zTXt"):
            yield "xmp", payload
        i += 12 + length


def webp_blocks(data):
    i = 12
    while i + 8 <= len(data):
        kind, length = struct.unpack("<4sI", data[i:i + 8])
        payload = data[i + 8:i + 8 + length]
        if kind == b"EXIF":
            yield "exif", payload[6:] if payload.startswith(b"Exif\0\0") else payload
        elif kind == b"XMP ":
            yield "xmp", payload
        i += 8 + length + (length & 1)


def has_location(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] == b"\xff\xd8":
        blocks = jpeg_blocks(data)
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        blocks = png_blocks(data)
    elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        blocks = webp_blocks(data)
    else:
        return False
    for kind, payload in blocks:
        if kind == "exif" and exif_has_gps(payload):
            return True
        if kind == "xmp" and XMP_GPS.search(payload):
            return True
    return False


def images(roots):
    for root in roots:
        if os.path.isfile(root):
            yield root
            continue
        for directory, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if os.path.splitext(name)[1].lower() in EXTENSIONS:
                    yield os.path.join(directory, name)


def main():
    found = [p for p in images(sys.argv[1:] or ["."]) if has_location(p)]
    for path in found:
        print(f"{path} has GPS location data; remove it without re-encoding: exiftool -gps:all= -xmp:all= -overwrite_original {path}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
