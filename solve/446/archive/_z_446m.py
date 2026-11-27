import sys, os, re, time, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/tmp/cylab_eps/t446"
proc = subprocess.Popen(["./game"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=CWD)
fd = proc.stdout.fileno()
os.set_blocking(fd, False)
seq = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d" + "s" * 29 + "d" * 89
proc.stdin.write(seq.encode())
proc.stdin.flush()
time.sleep(4)
out = b""
while True:
    try:
        c = os.read(fd, 65536)
    except BlockingIOError:
        break
    except Exception:
        break
    if not c:
        break
    out += c
txt = out.decode("utf-8", "replace")
proc.terminate()
# garder les messages non-grille
msgs = [l for l in txt.split("\n") if not set(l) <= set(".#@X ") and l.strip()]
print("messages:", msgs[-12:])
print("\n'You win' present:", "You win" in txt)
print("'Level: 2' present:", "Level: 2" in txt)
print("\nfin brute:", txt[-300:])
