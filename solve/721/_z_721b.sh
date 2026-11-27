#!/bin/bash
IMG=/mnt/c/Users/arnol/Downloads/partition4.img
echo "=== recherche brute du motif academy{ ==="
timeout 300 grep -aob "academy{" "$IMG" | head -10
echo "=== fls (racine) ==="
fls -p "$IMG" 2>/dev/null | head -25
echo "=== fichiers interessants (recursif) ==="
timeout 300 fls -r -p "$IMG" 2>/dev/null | grep -iE "flag|secret|home|root|bash_history|txt" | head -25
