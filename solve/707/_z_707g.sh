#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/707"
cd "$D" || exit 1
echo "=== grep academy dans l'image ==="
timeout 600 grep -aoE 'academy\{[^}]{5,80}\}|picoCTF\{[^}]{5,80}\}' disk.img 2>/dev/null | sort -u | head -10
echo "=== grep pico/academy generique ==="
timeout 300 grep -ao 'academy' disk.img 2>/dev/null | head -3
