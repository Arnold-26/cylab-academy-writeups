import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PAYLOAD = b"""0!:+:+::**00p00g00!:v
v+:::!0p<+++::*:+::+<
>:++:+:+ +:0>0gg,:v
00g0!-00^ ^0:-!0_
"""
s = socket.create_connection(("mars.cylabacademy.net", 31689), timeout=15)
s.settimeout(6)
time.sleep(0.6)
try:
    print("banner:", s.recv(4096).decode("utf-8", "replace"))
except Exception:
    pass
s.sendall(PAYLOAD)
time.sleep(1.5)
out = b""
try:
    while True:
        c = s.recv(4096)
        if not c:
            break
        out += c
except Exception:
    pass
print("=== SORTIE ===")
print(repr(out[:600]))
print(out.decode("utf-8", "replace")[:600])
m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", out)
if m:
    print("FLAG:", m.group(0).decode())
s.close()
