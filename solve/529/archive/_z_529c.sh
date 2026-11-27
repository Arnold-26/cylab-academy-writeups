#!/bin/bash
echo "=== occurrences apk / download ==="
grep -oiE '[^"'"'"' ]*\.apk|/download[^"'"'"' ]*|href="[^"]*"' /tmp/pb.html | sort -u | head -25
echo "=== titres / texte visible ==="
python3 - <<'EOF'
import re, html
t = open('/tmp/pb.html', encoding='utf-8', errors='replace').read()
t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
t = re.sub(r'<[^>]+>', '\n', t)
t = html.unescape(t)
lines = [l.strip() for l in t.split('\n') if l.strip()]
for l in lines[:40]:
    print("  ", l[:150])
EOF
