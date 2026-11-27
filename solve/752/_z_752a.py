import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
try:
    r = s.get(BASE, timeout=20)
    print("status:", r.status_code, "| len:", len(r.text))
    print(r.text[:1500])
    print("\n=== formulaires ===")
    for m in re.finditer(r"<form[^>]*>|<input[^>]*>|<a [^>]*href=\"[^\"]*\"", r.text):
        print("  ", m.group(0)[:140])
except Exception as e:
    print("ERR", type(e).__name__, e)
