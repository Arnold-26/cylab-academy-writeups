import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST = "xebec.cylabacademy.net"
IMG = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\432_patched.jpg"
data = open(IMG, "rb").read()
print("image:", len(data))
s = socket.create_connection((HOST, 11534), timeout=20)
s.settimeout(15)
s.sendall(data)
try:
    s.shutdown(socket.SHUT_WR)
except Exception:
    pass
out = b""
t0 = time.time()
while time.time() - t0 < 15:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print(txt[:1800])
