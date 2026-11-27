import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://picoctfsolutions.com/picoctf-2021-x-marks-the-spot",
          "https://raw.githubusercontent.com/iounpaladin/picoctf-2021/master/web/x-marks-the-spot.md"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        if not u.endswith(".md"):
            t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
            t = re.sub(r"<[^>]+>", "\n", t)
            t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 10]
        print("##### %s (%s)" % (u[-40:], r.status_code))
        for l in lines[:28]:
            print("  ", l[:190])
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
