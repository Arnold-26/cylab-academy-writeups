#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 151_remote 2>/dev/null | sed -n '/<_start>:/,/^$/p' | grep -E "lea|call" | head -4
echo "=== fonctions detectees ==="
objdump -d -Mintel 151_remote 2>/dev/null | grep -E "^[0-9a-f]+ <" | head -20
echo "=== recherche des references a Password / flag ==="
python3 - <<'EOF'
d = open('151_remote','rb').read()
for s in (b'Password:', b'Flag file not found', b'flag'):
    i = d.find(s)
    print(s, 'offset', hex(i) if i >= 0 else None)
EOF
