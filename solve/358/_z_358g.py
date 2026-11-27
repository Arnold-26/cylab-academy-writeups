import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picoctf-2023-more-sqli", timeout=30, verify=False)
t = r.text
t2 = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
t2 = re.sub(r"<[^>]+>", "\n", t2)
t2 = html.unescape(t2)
lines = [l.strip() for l in t2.split("\n") if l.strip() and len(l.strip()) > 20]
for l in lines:
    if re.search(r"(OR 1|username|password|UNION|search|flag|sqlite|mysql|inject|payload)", l, re.I):
        print(" ", l[:220])
