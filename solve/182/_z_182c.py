import sys, re, requests, urllib3, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
base = "http://xebec.cylabacademy.net:33257/"
r = requests.get(base + "ZoRd23o0wd", timeout=20)
p = B / "182_wasm.bin"
p.write_bytes(r.content)
print("taille wasm:", len(r.content), "| magic:", r.content[:4])
# chaines ascii
for m in re.finditer(rb"[ -~]{4,80}", r.content):
    print("  ", m.group(0)[:80].decode("latin-1"))
