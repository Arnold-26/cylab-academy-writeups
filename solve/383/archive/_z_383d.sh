#!/bin/bash
cd /tmp/cylab_eps/g383 || exit 1
echo "=== flag dans les textes dechiffres ==="
grep -aoE "academy\{[^}]*\}|picoCTF\{[^}]*\}" p1.txt p2.txt p3.txt 2>/dev/null | head
grep -aoE "academy\{[^}]*\}|picoCTF\{[^}]*\}" *.txt *.bin 2>/dev/null | head
echo "=== recherche du flag dans le disque extrait (si present) ==="
cd .. || exit 1
[ -d g383disk ] && grep -raoE "academy\{[^}]{4,60}\}" g383disk 2>/dev/null | head -5
ls -d g383* 2>/dev/null
echo "=== strings sur l image disque : mots de passe / irclogs ==="
strings -n 8 383_disk.img 2>/dev/null | grep -aiE "steghide|passphrase|password:|irc" | head -15
