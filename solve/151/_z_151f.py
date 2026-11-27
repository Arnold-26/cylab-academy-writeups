import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 11427
PW = "GpLaMjEWpVOjnnmkRGiledp6Mvcezxls"
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(8)
time.sleep(0.5)
out = b""
try:
    out = s.recv(8192)
except Exception:
    pass
print("banner:", out.decode("utf-8", "replace")[:200])
s.sendall((PW + "\n").encode())
time.sleep(1.0)
res = b""
try:
    while True:
        c = s.recv(8192)
        if not c:
            break
        res += c
except Exception:
    pass
txt = res.decode("utf-8", "replace")
print("=== REPONSE ===")
print(txt[:600])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else "non trouve")
s.close()
