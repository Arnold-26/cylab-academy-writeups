import sys, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/77695762a74381ca12a69932aab6c7a22e4dc95de92d0056f13a315ac133833b/b1g_mac.zip"
dest = B / "56_b1g_mac.zip"
if not (dest.exists() and dest.stat().st_size > 1000):
    r = requests.get(u, timeout=90, verify=False)
    dest.write_bytes(r.content)
print("zip:", dest.stat().st_size)
import zipfile
z = zipfile.ZipFile(dest)
for n in z.namelist():
    print("  ", n, z.getinfo(n).file_size)
