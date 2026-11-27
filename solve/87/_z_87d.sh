#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== icat inode 12 ==="
icat 87_suspicious.dd.sda1 12 2>/dev/null | head -30
echo "=== istat ==="
istat 87_suspicious.dd.sda1 12 2>/dev/null | head -12
