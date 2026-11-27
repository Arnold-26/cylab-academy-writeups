import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:27114/"
r = requests.get(BASE + "designer.js", timeout=20)
print("designer.js:", r.status_code, len(r.text))
print(r.text[:3000])
