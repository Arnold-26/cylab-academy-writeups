#!/bin/bash
cd /tmp || exit 1
echo "=== contenu de /etc/chat (inode 32716) ==="
icat t721.img 32716 2>/dev/null | od -c | head -6
echo "--- texte ---"
icat t721.img 32716 2>/dev/null
echo
echo "=== recherche de flags dans l image ==="
strings -n 6 t721.img 2>/dev/null | grep -aoE "academy\{[^}]*\}" | head -5
