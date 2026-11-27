#!/bin/bash
cd /tmp/cylab_eps/m528/528_minions || exit 1
echo "=== layouts ==="
ls res/layout* 2>/dev/null | head
echo "=== activity_main.xml ==="
cat res/layout/activity_main.xml 2>/dev/null | head -60
echo "=== values specifiques ==="
for f in res/values/*.xml; do
  case "$f" in *styles*|*colors*|*dimens*|*ids*|*attrs*|*themes*) continue;; esac
  echo "--- $f ---"; head -30 "$f"
done
echo "=== recherche 'minion' / suspects dans le smali de l'app ==="
grep -rl "picoctfimage" --include=*.smali . | head -10
