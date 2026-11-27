import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picoctf-2025-apriti-sesamo", timeout=30, verify=False)
t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 20]
for l in lines[:12]:
    print("  ", l[:190])
print("\n=== technique ===")
for l in lines:
    if re.search(r"(backup|\.bak|sha1|sha-1|hash|0e|magic|loose|==|login|admin|payload|curl)", l, re.I):
        print("  ", l[:190])
