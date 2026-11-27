import sys, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
u = "https://challenge-files.cylabacademy.net/library/6fbc1d16c68bad74917fdc29beda04f94cc4d60168d9007458d6a4d000bbd2a3/nginx.conf"
dest = B / "725_nginx.conf"
if not (dest.exists() and dest.stat().st_size > 50):
    r = requests.get(u, timeout=30, verify=False)
    dest.write_bytes(r.content)
print("taille:", dest.stat().st_size)
print(dest.read_text(errors="replace"))
