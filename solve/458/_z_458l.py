import subprocess, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps"
base = b"academy{0n3_bi7_4t_a_7im3}"
print("len base:", len(base))
found = None
for c in range(256):
    payload = base + bytes([c]) + b"\n"
    try:
        p = subprocess.run(["./458_perplexed"], input=payload, capture_output=True, cwd=CWD, timeout=5)
        out = p.stdout + p.stderr
        if b"Correct" in out:
            found = c
            print("TROUVE octet 27 = 0x%02x (%r)" % (c, chr(c)))
            break
    except Exception:
        pass
print("resultat:", found)
