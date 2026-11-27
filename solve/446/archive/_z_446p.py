import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps/t446"
for seq in ("p" * 10, "p" * 5, "pppppppp"):
    p = subprocess.run(["./game"], input=seq.encode() + b"\n", capture_output=True, cwd=CWD, timeout=120)
    out = p.stdout.decode("utf-8", "replace")
    lv = re.findall(r"Level: (\d+)", out)
    print(f"seq={seq[:10]}... niveaux vus: {sorted(set(lv))} | You win: {'You win' in out} | flag: {re.findall(r'(?:academy|picoCTF)\{[^}]*\}', out)[:1]}")
    print("  fin:", out[-200:].replace("\n", " | ")[:250])
