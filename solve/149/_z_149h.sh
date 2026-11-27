#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== chaines autour du controle ==="
strings -n 4 -t x 149_checkpass | grep -aiE "invalid|length|correct|wrong|flag|password|academy|great|nice|good" | head -15
echo "=== references aux chaines dans le code ==="
python3 - <<'PYEOF'
d = open('/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/149_checkpass','rb').read()
for pat in (b'Invalid length', b'correct', b'flag', b'password'):
    i = d.find(pat)
    print(pat, "-> offset fichier", hex(i) if i >= 0 else None)
PYEOF
echo "=== essai avec 32 et 40 caracteres heterogenes ==="
for p in "0123456789012345678901234567890123" "abcdefghijklmnopqrstuvwxyz0123456789" ; do
  echo "--- ${p:0:12}... ---"
  timeout 5 ./149_checkpass "$p" 2>&1 | head -3
done
