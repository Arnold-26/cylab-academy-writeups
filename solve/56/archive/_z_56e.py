import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://picoctfsolutions.com/picoctf-2019-b1g-mac",
          "https://picoctf2019.haydenhousen.com/forensics/b1g_mac"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 25]
        print("##### %s (%s)" % (u[-40:], r.status_code))
        for l in lines[:18]:
            print("  ", l[:200])
        print()
    except Exception as e:
        print("ERR", type(e).__name__, u[-40:])
