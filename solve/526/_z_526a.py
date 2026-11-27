import sys, subprocess, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_v")


def mnt(p):
    s = str(p).replace("\\", "/")
    return "/mnt/" + s[0].lower() + s[2:]


def sh(c, t=300):
    r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc", c],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=t)
    return (r.stdout or "") + (r.stderr or "")


print("=== 526 vuln.c ===")
print(sh(f"cat {mnt(D)}/526/vuln.c").strip()[:1200])
