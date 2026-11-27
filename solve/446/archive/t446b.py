import subprocess
def build():
    s = bytearray()
    s += b"l\x00"; s += b"w"*3; s += b"a"*5; s += b"w"; s += b"a"*5
    s += b"l\xff" + b"a"; s += b"a"*3; s += b"l\xf5" + b"a"
    s += b"l\x00" + b"a"*4; s += b"a"*3; s += b"l\x05" + b"a"
    s += b"l\x00" + b"a"*31; s += b"l\xfe" + b"a"
    return bytes(s)
seq = build()
r = subprocess.run(["./game"], input=seq, capture_output=True, timeout=120)
out = r.stdout.decode("latin1","replace")
mv = sum(1 for c in seq if c in b"wasd")
print("rc", r.returncode, "prints", out.count("Level:"), "moves", mv)
print("stderr", r.stderr[:200])
print("lastpos", out.split("Player position: ")[-1][:12] if "Player position: " in out else None)
for l in out.splitlines()[-33:-27]:
    print(repr(l[:95]))
