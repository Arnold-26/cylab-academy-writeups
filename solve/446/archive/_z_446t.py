import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps/t446"
EXPLOIT = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
for n in (4, 5, 6):
    seq = (EXPLOIT + "p") * n
    try:
        p = subprocess.run(["./game"], input=seq.encode() + b"\n", capture_output=True,
                           cwd=CWD, timeout=180)
        out = p.stdout.decode("utf-8", "replace")
        lv = sorted(set(re.findall(r"Level: (\d+)", out)))
        fl = re.findall(r"(?:academy|picoCTF)\{[^}]*\}", out)
        print(f"{n} rep: niveaux={lv} win={'You win' in out} flag={fl[:1]}")
        print("   fin:", out[-180:].replace("\n", " | ")[:200])
    except subprocess.TimeoutExpired:
        print(f"{n} rep: TIMEOUT")
