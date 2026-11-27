import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
base = "http://xebec.cylabacademy.net:33257/"
r = requests.get(base + "rqe4VVml5W.js", timeout=20)
print("taille JS:", len(r.text))
print(r.text[:3000])
