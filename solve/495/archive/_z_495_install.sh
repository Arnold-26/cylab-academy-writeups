#!/bin/bash
python3 -m pip install --quiet --break-system-packages monocypher requests 2>&1 | tail -3
python3 - <<'EOF'
import monocypher, requests
print("monocypher OK:", monocypher.__file__)
print("requests OK")
EOF
