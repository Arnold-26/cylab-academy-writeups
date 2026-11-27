import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
url = "https://medium.com/@affanhaxor/sqlmap-1-cylab-security-academy-write-up-exploiting-sql-injection-and-accessing-protected-data-b86c4fa5955f"
for u in (url, url + "?format=json"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        print("### %s -> %s (%d o)" % (u[-40:], r.status_code, len(r.text)))
        t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 25]
        for l in lines[:25]:
            print("  ", l[:200])
        break
    except Exception as e:
        print("ERR", type(e).__name__)
