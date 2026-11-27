import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://blog.nickchen120235.dev/2022/04/19/checkpass.html",
          "https://picoctfsolutions.com/picoctf-2021-checkpass"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 4]
        print("##### " + u[-36:])
        for l in lines[:50]:
            print("  ", l[:190])
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
