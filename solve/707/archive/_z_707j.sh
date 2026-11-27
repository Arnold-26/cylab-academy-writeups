#!/bin/bash
cd /tmp/repo707 || exit 1
export HOME=/tmp
echo "=== git log ==="
git --git-dir=.git log --all --oneline 2>&1 | head -20
echo "=== recherche flag dans tout l'historique ==="
git --git-dir=.git log --all -p 2>&1 | grep -aoE 'academy\{[^}]*\}|picoCTF\{[^}]*\}' | head -5
echo "=== objets non references ==="
git --git-dir=.git fsck --lost-found 2>&1 | head -10
echo "=== recherche dans les objets ==="
for o in .git/objects/*/*; do
  git --git-dir=.git cat-file -p "$(echo $o | sed 's|.git/objects/||; s|/||')" 2>/dev/null | grep -aoE 'academy\{[^}]*\}|picoCTF\{[^}]*\}' | head -1
done | head -5
