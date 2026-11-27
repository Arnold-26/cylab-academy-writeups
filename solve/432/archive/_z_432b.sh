#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== tous les tags (noms) ==="
exiftool -a -u -g1 432_original.jpg 2>/dev/null | awk -F: '{print $1}' | sort -u | head -60
echo
echo "=== vignette / preview ==="
exiftool -b -ThumbnailImage 432_original.jpg > /tmp/thumb.jpg 2>/dev/null; ls -la /tmp/thumb.jpg 2>/dev/null
exiftool -b -PreviewImage 432_original.jpg > /tmp/prev.jpg 2>/dev/null; ls -la /tmp/prev.jpg 2>/dev/null
echo "=== segments JPEG (APPn) ==="
python3 - <<'EOF'
d = open('432_original.jpg','rb').read()
print("taille:", len(d))
j = 2
while j < len(d)-4:
    if d[j] != 0xFF:
        j += 1
        continue
    m = d[j+1]
    if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
        j += 2
        continue
    ln = int.from_bytes(d[j+2:j+4], 'big')
    print("  FF%02X len=%d" % (m, ln), end="")
    if 0xE0 <= m <= 0xEF:
        tag = d[j+4:j+2+ln][:32]
        print("  ->", tag.split(b'\x00')[0][:24])
    else:
        print()
    j += 2 + ln
    if m == 0xDA:
        print("  (SOS, fin des segments)")
        break
EOF
