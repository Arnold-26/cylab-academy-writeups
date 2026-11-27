import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = "http://chatelaine.cylabacademy.net:29796"
paths = ["/robots.txt", "/flag", "/flag.txt", "/api", "/api/flag", "/health", "/status",
         "/admin", "/.env", "/config", "/debug", "/ssrf", "/proxy", "/fetch", "/url", "/north", "/south"]
for p in paths:
    try:
        r = requests.get(base + p, timeout=10, verify=False)
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text or ""))[:120]
        print(f"{p} -> {r.status_code} {txt!r}")
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text or "")
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print(p, "err", type(e).__name__)
