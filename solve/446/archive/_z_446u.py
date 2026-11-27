import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps/t446"
EXPLOIT = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
seq = (EXPLOIT + "p") * 5
with open("/tmp/bg3out.txt", "wb") as f:
    p = subprocess.run(["./game"], input=seq.encode() + b"\n", stdout=f,
                       stderr=subprocess.STDOUT, cwd=CWD, timeout=200)
out = open("/tmp/bg3out.txt", "rb").read().decode("utf-8", "replace")
lv = sorted(set(re.findall(r"Level: (\d+)", out)))
fl = re.findall(r"(?:academy|picoCTF)\{[^}]*\}", out)
print("taille:", len(out))
print("niveaux:", lv)
print("win:", "You win" in out)
print("flag:", fl[:3])
print("fin:", out[-250:].replace("\n", " | ")[:280])
