#!/bin/bash
cd /tmp/cylab_eps || exit 1
exiftool -b -ThumbnailImage 432_original.jpg > 432_thumb.jpg 2>/dev/null
ls -la 432_thumb.jpg
file 432_thumb.jpg
echo "=== strings de la vignette ==="
strings -n 6 432_thumb.jpg | head -10
echo "=== octets utiles ==="
python3 - <<'EOF'
d = open('432_thumb.jpg','rb').read()
print("taille:", len(d), "| debut:", d[:4].hex())
i = d.rfind(b'\xff\xd9')
print("EOI:", i, "| apres:", len(d)-(i+2) if i>=0 else -1)
if i >= 0 and len(d) > i+2:
    print("data:", d[i+2:i+2+120])
EOF
