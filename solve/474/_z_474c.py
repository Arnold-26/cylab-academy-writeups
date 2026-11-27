import sys, re, time, socket, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 24956
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
names = [l.strip() for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]
UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

s = socket.create_connection((HOST, PORT), timeout=25)
s.settimeout(8)
time.sleep(0.6)
out = b""
try:
    while True:
        c = s.recv(16384)
        if not c:
            break
        out += c
        if b"to do?" in out or b"?" in out[-60:]:
            break
except socket.timeout:
    pass
banner = out.decode("utf-8", "replace")
print("=== banner ===")
print(banner[:800])
s.close()
