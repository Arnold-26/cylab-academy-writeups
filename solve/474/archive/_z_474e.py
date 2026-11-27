import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picoctf-2025-guess-my-cheese-part-2", timeout=30, verify=False)
t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 25]
for l in lines[:20]:
    print("  ", l[:200])
print("\n=== indices ===")
for l in lines:
    if re.search(r"(hash|sha|md5|salt|wordlist|brute|dictionn|dictionar|list of cheese|crack)", l, re.I):
        print("  ", l[:200])
