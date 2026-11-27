#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== artefacts 383 ==="
ls -la 383* 2>/dev/null | head -10
echo "=== dossier g383 ==="
ls -la g383 2>/dev/null | head -20
find . -maxdepth 3 -iname "*.bmp" -newer /dev/null 2>/dev/null | head -20
echo "=== recherche des bmp dans l'image (si extraite) ==="
[ -d g383 ] && find g383 -type f | head -30
