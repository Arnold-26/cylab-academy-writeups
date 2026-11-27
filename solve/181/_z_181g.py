import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://7rocky.github.io/en/ctf/picoctf/binary-exploitation/bizz-fuzz/",
          "https://picoctfsolutions.com/picoctf-2021-bizz-fuzz"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 14]
        print("##### %s (%s)" % (u[-38:], r.status_code))
        for l in lines[:26]:
            print("  ", l[:180])
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
