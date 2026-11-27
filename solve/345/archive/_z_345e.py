import subprocess, re, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps"
os.makedirs(CWD + "/t345", exist_ok=True)
subprocess.run(["cp", "-f", CWD + "/345_game", CWD + "/t345/game"], check=False)
open(CWD + "/t345/flag.txt", "w").write("academy{TEST345}\n")
# aller en (0,-4) puis (29,89)
seq = "w" * 4 + "a" * 8 + "s" * 29 + "d" * 93
print("seq len:", len(seq))
p = subprocess.run(["./game"], input=seq.encode() + b"\n", capture_output=True,
                   cwd=CWD + "/t345", timeout=120)
out = p.stdout.decode("utf-8", "replace")
print("taille:", len(out))
fl = re.findall(r"(?:academy|picoCTF)\{[^}]*\}", out)
print("flag:", fl[:2])
print("fin:", out[-400:].replace("\n", " | ")[:450])
