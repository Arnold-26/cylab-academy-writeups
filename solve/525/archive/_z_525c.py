import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picomini-by-cmu-africa-input-injection-1", timeout=30, verify=False)
t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 20]
for l in lines[:14]:
    print("  ", l[:190])
print("\n=== payload / offsets ===")
for l in lines:
    if re.search(r"(payload|offset|cat flag|/bin/sh|overflow|strcpy|command|byte|24|28|32|padding)", l, re.I):
        print("  ", l[:190])
