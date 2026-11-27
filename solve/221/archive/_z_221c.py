import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PATH = b"rrrrrlrlrlrlrllddddddlddrrddrrrrdddrruuuruuuuuuurrddddddddlddrd\n"
s = socket.create_connection(("mars.cylabacademy.net", 31259), timeout=15)
s.settimeout(6)
time.sleep(0.6)
try:
    print("banner:", s.recv(4096).decode("utf-8", "replace"))
except Exception:
    pass
s.sendall(PATH)
time.sleep(1.2)
out = b""
try:
    while True:
        c = s.recv(4096)
        if not c:
            break
        out += c
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("=== SORTIE ===")
print(txt[:800])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
if m:
    print("FLAG:", m.group(0))
s.close()
