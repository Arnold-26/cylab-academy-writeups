import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "chatelaine.cylabacademy.net", 26060
s = socket.create_connection((host, port), timeout=15)
s.settimeout(5)
print("connecte")
out = b""
t0 = time.time()
while time.time() - t0 < 5:
    try:
        c = s.recv(4096)
        if not c:
            print("ferme par le serveur")
            break
        out += c
    except socket.timeout:
        break
print("recu sans rien envoyer:", repr(out[:200]))
s.sendall(b"hello\n")
time.sleep(0.5)
out2 = b""
t0 = time.time()
while time.time() - t0 < 5:
    try:
        c = s.recv(4096)
        if not c:
            break
        out2 += c
    except socket.timeout:
        break
print("apres 'hello':", repr(out2[:300]))
s.close()
