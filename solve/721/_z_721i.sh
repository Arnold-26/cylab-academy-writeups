#!/bin/bash
echo "=== taille decompressee annoncee par gzip ==="
gzip -l /mnt/c/Users/arnol/Downloads/timeline-1-partition4.img.gz 2>/dev/null
echo "=== taille de partition4.img ==="
stat -c%s /mnt/c/Users/arnol/Downloads/partition4.img
echo "=== occurrence 'flag' dans l'image ==="
timeout 300 grep -aobi "flag" /mnt/c/Users/arnol/Downloads/partition4.img | head -15
