#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== API du module ==="
python3 -c "import sstv, inspect; print([x for x in dir(sstv) if not x.startswith('_')])" 2>&1 | head -3
echo "=== CLI via module ==="
python3 -m sstv --help 2>&1 | head -12
