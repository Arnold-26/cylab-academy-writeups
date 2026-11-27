import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://picoctfsolutions.com/picoctf-2021-binary-gauntlet-1",
          "https://tristanwhite.me/blog/2024/10/15/binary-gauntlet-1/"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 12]
        print("##### %s (%s)" % (u[-40:], r.status_code))
        for l in lines[:30]:
            print("  ", l[:190])
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
