import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:47074"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r = s.get(A + "/", timeout=20)
fields = re.findall(r'<(?:input|form)[^>]*>', r.text)
print("=== champs / form ===")
for f in fields:
    print("  ", f[:150])
# indices dans le HTML
print("\n=== extrait autour du form ===")
i = r.text.lower().find("<form")
print(r.text[i:i + 700] if i >= 0 else "(pas de form)")
