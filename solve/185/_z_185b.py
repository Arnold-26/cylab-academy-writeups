import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
r = requests.get(BASE, timeout=20)
print("status:", r.status_code, "| len:", len(r.text))
print(r.text[:1200])
print("\n=== formulaires ===")
for m in re.finditer(r"<form[^>]*>", r.text):
    print(m.group(0))
for m in re.finditer(r"<input[^>]*>", r.text):
    print(m.group(0))
