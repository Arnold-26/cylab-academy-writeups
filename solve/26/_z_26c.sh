#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
python3 - <<'EOF' 2>&1 | tail -25
import sstv
img = sstv.decode_from_wav("26_message.wav")
print("image:", img.size if hasattr(img, "size") else type(img))
img.save("26_decoded.png")
print("saved 26_decoded.png")
EOF
