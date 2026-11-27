import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = "http://xebec.cylabacademy.net:30999"
r = requests.get(base, timeout=15, verify=False)
html = r.text or ""
js = re.findall(r'src=["\']([^"\']+\.js)["\']', html)
print("scripts:", js)
for j in js:
    if "stockfish" in j or "script" in j or "app" in j or "main" in j:
        rr = requests.get(base + "/" + j.lstrip("/"), timeout=15, verify=False)
        print(f"\n=== {j} ===")
        print((rr.text or "")[:1500])
# aussi chercher un script inline
inline = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S))
print("\n=== inline ===")
print(inline[:2000])
