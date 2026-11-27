#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== type ==="
file 87_suspicious.dd.sda1 | cut -c1-150
echo "=== flag direct ==="
grep -aoE "(academy|picoCTF)\{[^}]{4,80}\}" 87_suspicious.dd.sda1 | head -5
echo "=== fsstat ==="
fsstat 87_suspicious.dd.sda1 2>/dev/null | grep -E "File System Type|Volume Name|Last Mounted" | head -4
echo "=== fichiers racine ==="
fls -r -p 87_suspicious.dd.sda1 2>/dev/null | head -25
