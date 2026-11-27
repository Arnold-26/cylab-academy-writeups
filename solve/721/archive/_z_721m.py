import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picoctf-2026-timeline-1", timeout=30, verify=False,
                 headers={"User-Agent": "Mozilla/5.0"})
t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 20]
print("HTTP", r.status_code, "lignes:", len(lines))
for l in lines[:22]:
    print("  ", l[:200])
