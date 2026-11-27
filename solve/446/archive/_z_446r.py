import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps/t446"
EXPLOIT = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
seq = (EXPLOIT + "p") * 6
print("longueur:", len(seq))
p = subprocess.run(["./game"], input=seq.encode() + b"\n", capture_output=True, cwd=CWD, timeout=300)
out = p.stdout.decode("utf-8", "replace")
lv = re.findall(r"Level: (\d+)", out)
fl = re.findall(r"(?:academy|picoCTF)\{[^}]*\}", out)
print("niveaux:", sorted(set(lv)))
print("win:", "You win" in out)
print("flag:", fl[:2])
print("fin:", out[-300:].replace("\n", " | ")[:320])
