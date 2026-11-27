#!/bin/bash
cd /tmp || exit 1
echo "=== flag direct ==="
grep -aoE "academy\{[^}]{2,80}\}" t413full.img 2>/dev/null | head -5
echo "=== occurrences de innocuous-file.txt ==="
grep -aob "innocuous-file.txt" t413full.img 2>/dev/null | head -20
echo "=== occurrences de its-all-in-the-name ==="
grep -aob "its-all-in-the-name" t413full.img 2>/dev/null | head -10
