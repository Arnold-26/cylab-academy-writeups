#!/bin/bash
cd /tmp/cylab_eps || exit 1
pip3 install --quiet sstv 2>&1 | tail -3
python3 -c "import sstv; print('sstv ok', sstv.__file__)" 2>&1 | tail -2
echo "=== decode ==="
python3 - <<'EOF' 2>&1 | tail -20
import sstv
from sstv import decode
from PIL import Image
import wave, numpy as np
p = "26_message.wav"
w = wave.open(p, "rb")
print("canaux:", w.getnchannels(), "rate:", w.getframerate(), "frames:", w.getnframes())
w.close()
try:
    img = decode(p, "robot36")
    img.save("26_robot36.png")
    print("robot36 ->", img.size)
except Exception as e:
    print("robot36 err:", type(e).__name__, e)
EOF
