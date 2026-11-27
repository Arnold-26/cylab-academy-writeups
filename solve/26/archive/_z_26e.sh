#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== deja installe ? ==="
python3 -c "import sstv; print('sstv module OK', sstv.__file__)" 2>&1 | head -2
which sstv 2>/dev/null
echo "=== installation ==="
timeout 300 pip3 install --quiet sstv 2>&1 | tail -3
python3 -c "import sstv; print('module OK')" 2>&1 | head -2
ls /usr/local/bin/sstv /root/.local/bin/sstv 2>/dev/null
