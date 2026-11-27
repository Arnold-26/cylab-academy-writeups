import sys, struct, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BIN = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\36_no_auth_mistery"
OUT = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\36_investigation-encoded-2-output"
d = open(BIN, "rb").read()
# localiser secret et matrix via readelf
outp = subprocess.run(["wsl", "-d", "kali-linux", "--", "readelf", "-sW",
                       "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/36_no_auth_mistery"],
                      capture_output=True, text=True).stdout
for line in outp.splitlines():
    if any(k in line for k in ("secret", "matrix", "buff")):
        print(line.strip())
print("taille binaire:", len(d))
enc = open(OUT, "rb").read()
print("output:", len(enc), "octets ->", enc.hex())
