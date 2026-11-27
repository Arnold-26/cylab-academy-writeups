import subprocess, re, sys
def build():
    s = bytearray()
    s += b"l\x00"; s += b"w"*3; s += b"a"*5; s += b"w"; s += b"a"*5
    s += b"l\xff" + b"a"; s += b"a"*3; s += b"l\xf5" + b"a"
    s += b"l\x00" + b"a"*4; s += b"a"*3; s += b"l\x05" + b"a"
    s += b"l\x00" + b"a"*31; s += b"l\xfe" + b"a"
    return bytes(s)
seq = build()
try:
    r = subprocess.run(["./game"], input=seq, capture_output=True, timeout=280)
    out = r.stdout.decode("latin1","replace"); rc = r.returncode
except subprocess.TimeoutExpired as e:
    out = (e.stdout or b"").decode("latin1","replace"); rc = "TIMEOUT"
pos = re.findall(r"Player position: (\d+) (\d+)", out)
vals = re.findall(r"Lives left: (-?\d+)", out)
print("rc", rc, "prints", len(pos))
print("first lives:", vals[:3], "last lives:", vals[-3:])
print("FLAG:", [l for l in out.splitlines() if "FLAG" in l][:3])
print("obstacle:", "obstacle" in out, "gameover:", "No more lives" in out)
