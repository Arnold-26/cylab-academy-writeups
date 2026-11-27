import sys, json, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
H = "http://chatelaine.cylabacademy.net:15656"
print("GET /", requests.get(H + "/", timeout=15).status_code)
r = requests.post(H + "/flag", json={"flag1": "x", "flag2": "y"}, timeout=20)
print("POST /flag ->", r.status_code, r.text[:200])
r = requests.post(H + "/check", json={"circuit": []}, timeout=40)
print("POST /check [] ->", r.status_code, r.text[:300])
r = requests.post(H + "/check", json={"circuit": [{"input1": 0xfff, "input2": 0xfff, "output": 0xf000}]}, timeout=40)
print("POST /check 1gate ->", r.status_code, r.text[:300])
