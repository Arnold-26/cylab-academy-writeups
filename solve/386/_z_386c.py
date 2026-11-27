import sys, socket, time, zipfile, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
# 1) le service
s = socket.create_connection(("xebec.cylabacademy.net", 12383), timeout=15)
s.settimeout(6)
time.sleep(0.5)
out = b""
try:
    out = s.recv(8192)
except Exception:
    pass
print("=== SERVICE ===")
print(out.decode("utf-8", "replace")[:1200])
s.close()
# 2) le modele
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
z = zipfile.ZipFile(B / "386_Virtual-Machine-1.zip")
name = z.namelist()[0]
data = z.read(name).decode("utf-8", "replace")
print("\n=== MODELE ===")
print("taille:", len(data))
geos = re.findall(r'<geometry[^>]*id="([^"]+)"', data)
print("geometries:", geos)
nodes = re.findall(r'<node[^>]*name="([^"]+)"', data)
print("noeuds:", nodes[:25])
