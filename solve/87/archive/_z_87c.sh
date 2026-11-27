#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== fichiers suspects / hors systeme ==="
fls -r -p 87_suspicious.dd.sda1 2>/dev/null | grep -viE "tce/optional|boot/grub|usr/(share|lib|bin|local)|lib/modules|etc/|sbin/" | head -40
echo "=== fichiers supprimes ==="
fls -r -p 87_suspicious.dd.sda1 2>/dev/null | grep -E "^\*|\(deleted\)" | head -20
