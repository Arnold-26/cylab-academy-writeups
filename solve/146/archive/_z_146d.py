import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://picoctfsolutions.com/picoctf-2021-cache-me-outside",
          "https://raw.githubusercontent.com/Dvd848/CTFs/master/discussions/29.md"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        if not u.endswith(".md"):
            t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
            t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
            t = re.sub(r"<[^>]+>", "\n", t)
            t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 18]
        print("##### %s (%s)" % (u[-45:], r.status_code))
        for l in lines[:30]:
            print("  ", l[:210])
        print()
    except Exception as e:
        print("ERR", type(e).__name__, u[-40:])
