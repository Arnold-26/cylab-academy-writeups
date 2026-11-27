#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== appels a win (0x804975d) ==="
objdump -d -Mintel 346_game 2>/dev/null | grep -B8 "call.*804975d" | head -30
echo "=== chaine You win ==="
objdump -d -Mintel 346_game 2>/dev/null | grep -B4 -A4 "80496" | grep -iE "you win" | head -3
python3 - <<'PYEOF'
d = open("/tmp/cylab_eps/346_game",'rb').read()
for s in (b"You win!", b"flag.txt", b"End tile position"):
    print(s, hex(d.find(s)))
PYEOF
