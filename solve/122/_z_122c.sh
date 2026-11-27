#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== occurrences des chaines ==="
python3 - <<'EOF'
d = open('122_brute','rb').read()
for s in (b'input the flag:', b'Correct!', b'Incorrect.', b'checking solution'):
    i = d.find(s)
    print(s, '-> offset fichier', hex(i) if i>=0 else None)
EOF
echo "=== fonctions ==="
nm 122_brute 2>/dev/null | grep -E " [TtWw] " | head -20
echo "=== main ==="
objdump -d -Mintel 122_brute 2>/dev/null | grep -E "^[0-9a-f]+ <" | head -15
