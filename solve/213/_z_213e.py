import sys, struct, subprocess, time, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
cwd = "/tmp/cylab_eps"
open(os.path.join(cwd, "flag.txt"), "w").write("academy{LOCALTEST99}\n")
p = subprocess.Popen(["./213_chall"], cwd=cwd, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
time.sleep(0.3)
maps = open(f"/proc/{p.pid}/maps").read()
print("=== maps ===")
print(maps)
p.kill()
