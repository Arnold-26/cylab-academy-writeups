import subprocess
BIN = "/tmp/cylab_eps/149_checkpass"
pw = "academy{" + "A"*32 + "}"
r = subprocess.run(["valgrind", "--tool=cachegrind", "--cachegrind-out-file=/dev/null", BIN, pw],
                   capture_output=True, text=True)
print("returncode:", r.returncode)
print("--- stderr (20 dernieres lignes) ---")
for line in r.stderr.splitlines()[-20:]:
    print("  ", line)
print("--- stdout ---")
print(r.stdout[:300])
