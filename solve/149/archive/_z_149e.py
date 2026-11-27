import subprocess, sys, time, os
BIN = r"/tmp/cylab_eps/149_checkpass"
WSL = ["wsl", "-d", "kali-linux", "--"]


def run_local(pw):
    t0 = time.perf_counter()
    p = subprocess.run([BIN, pw], capture_output=True, text=True, timeout=10)
    dt = time.perf_counter() - t0
    return dt, (p.stdout + p.stderr).strip()


# test de longueurs croissantes
for n in list(range(1, 40)) + [50, 64, 80, 100]:
    pw = "A" * n
    try:
        dt, out = run_local(pw)
        tag = "LONGUEUR OK" if "Invalid length" not in out else ""
        if tag or n % 10 == 0:
            print("len=%-4d dt=%.4f -> %s %s" % (n, dt, out[:60], tag))
    except Exception as e:
        print("len", n, "ERR", type(e).__name__)
