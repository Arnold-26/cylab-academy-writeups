import sys, re, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps/t446"
# juste l'exploit des vies, puis on regarde le compteur
seq = "w" * 4 + "a" * 11 + "d" * 3
p = subprocess.run(["./game"], input=seq.encode() + b"\n", capture_output=True, cwd=CWD, timeout=60)
out = p.stdout.decode("utf-8", "replace")
lives = re.findall(r"Lives left: (-?\d+)", out)
print("compteurs de vies vus:", lives[:6], "…", lives[-3:] if lives else None)
print("dernier bloc:", out[-300:])
