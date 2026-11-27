#!/bin/bash
cd /tmp || exit 1
echo "=== bodyfile : fichiers de taille 49 ==="
fls -r -m / t721.img 2>/dev/null | awk -F'|' '$7 == 49 {print}' | head -20
echo "=== tous les fichiers sous home ==="
fls -r -p t721.img 2>/dev/null | grep -i "home/" | head -30
echo "=== tailles des fichiers sous home ==="
fls -r -m / t721.img 2>/dev/null | awk -F'|' '$2 ~ /home\// {printf "%s | size=%s | crtime=%s\n", $2, $7, $11}' | head -30
