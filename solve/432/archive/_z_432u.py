import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST = "xebec.cylabacademy.net"
IMG = r"/tmp/cylab_eps\432_patched.jpg"
data = open(IMG, "rb").read()
print("envoi de", len(data), "octets a 11287 ...")
s = socket.create_connection((HOST, 11287), timeout=30)
s.settimeout(20)
s.sendall(data)
try:
    s.shutdown(socket.SHUT_WR)
except Exception:
    pass
try:
    r = s.recv(4096)
    print("reponse submit:", r[:300])
except Exception as e:
    print("submit:", type(e).__name__)
s.close()
time.sleep(3)
print("\n=== validation (11534) ===")
s = socket.create_connection((HOST, 11534), timeout=30)
s.settimeout(20)
out = b""
t0 = time.time()
while time.time() - t0 < 20:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print(txt[-1600:])
