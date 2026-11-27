import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:32822/"
r = requests.get(BASE, timeout=20)
print("status:", r.status_code, "| len:", len(r.text), "| server:", r.headers.get("Server"))
print(r.text[:2000])
