import sys, json, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
try:
    r = requests.post("https://webhook.site/token", timeout=30,
                      headers={"Content-Type": "application/json"}, json={})
    print("token status:", r.status_code)
    print(r.text[:300])
    if r.status_code == 200:
        d = r.json()
        print("UUID:", d.get("uuid"))
except Exception as e:
    print("ERR", type(e).__name__, e)
