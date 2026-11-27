import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://picoctfsolutions.com/picoctf-2019-torrent-analyze",
          "https://7rocky.github.io/en/ctf/picoctf/forensics/torrent-analyze/"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 12]
        print("##### %s (%s)" % (u[-40:], r.status_code))
        for l in lines[:26]:
            print("  ", l[:180])
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
