import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps/t446"
EXPLOIT = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
for n in (1, 5, 8):
    seq = EXPLOIT + "p" * n
    p = subprocess.run(["./game"], input=seq.encode() + b"\n", capture_output=True, cwd=CWD, timeout=180)
    out = p.stdout.decode("utf-8", "replace")
    lv = re.findall(r"Level: (\d+)", out)
    fl = re.findall(r"(?:academy|picoCTF)\{[^}]*\}", out)
    print(f"p x{n}: niveaux={sorted(set(lv))} | win={'You win' in out} | flag={fl[:1]}")
    print("   fin:", out[-260:].replace("\n", " | ")[:280])
