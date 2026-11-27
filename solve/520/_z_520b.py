import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for url in ("https://picoctfsolutions.com/picomini-by-cmu-africa-crack-the-gate-1",):
    r = requests.get(url, timeout=30, verify=False)
    t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 25]
    print("=== writeup ===")
    for l in lines[:22]:
        print("  ", l[:200])
