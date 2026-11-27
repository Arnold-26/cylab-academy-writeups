import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "nm -D libc.so.6 2>/dev/null | grep -E ' (system|free|puts|printf|__libc_start_main)@@'"],
                     capture_output=True, text=True).stdout
print(out)
# verification de l'offset du leak
print("offset leak mesure: 0x%x" % (0x7ffff7e31fd0 - 0x7ffff7ddf000))
