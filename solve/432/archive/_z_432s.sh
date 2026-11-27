#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== exiftool sur le fichier patche ==="
exiftool 432_patched.jpg 2>&1 | grep -iE "error|warning|Time Stamp|Modify Date|Date/Time Original|Create Date|Sub Sec" | head -12
echo "=== verif integrite PNG/JPEG ==="
file 432_patched.jpg
