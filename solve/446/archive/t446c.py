import subprocess, re
seq = b"l\x00" + b"w"*3 + b"a"*5 + b"w" + b"a"*4
r = subprocess.run(["./game"], input=seq, capture_output=True, timeout=60)
out = r.stdout.decode("latin1","replace")
vals = re.findall(r"Lives left: (\d+)", out)
pos = re.findall(r"Player position: (\d+) (\d+)", out)
print("rc", r.returncode, "moves", sum(1 for c in seq if c in b"wasd"))
for i,(p,v) in enumerate(zip(pos, vals+[None]*9)):
    print(i, p, v)
