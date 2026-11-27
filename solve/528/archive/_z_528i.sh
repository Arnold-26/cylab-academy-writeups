#!/bin/bash
cd /tmp/cylab_eps/m528/528_minions 2>/dev/null || cd /tmp/cylab_eps/m528 || exit 1
echo "=== MainActivity.smali ==="
find . -name "MainActivity*.smali" | head -5
F=$(find . -name "MainActivity.smali" | head -1)
echo "--- $F ---"
cat "$F" 2>/dev/null | head -80
echo
echo "=== images de l'app ==="
find . -path ./original -prune -o -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.webp" \) -print 2>/dev/null | while read f; do
  case "$f" in *abc_*|*m3_*|*mtrl_*|*design_*|*ic_*|*notification_*|*tooltip*) continue;; esac
  ls -la "$f"
done | head -20
