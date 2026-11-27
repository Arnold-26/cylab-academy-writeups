import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picoctf-2025-guess-my-cheese-part-1", timeout=30, verify=False)
t = r.text
t2 = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
t2 = re.sub(r"<[^>]+>", "\n", t2)
t2 = html.unescape(t2)
lines = [l.strip() for l in t2.split("\n") if l.strip()]
# afficher tout ce qui ressemble aux etapes
for l in lines:
    if len(l) > 30 and re.search(r"(affine|modul|alphabet|key|a =|b =|inverse|decrypt|letters|upper|lower|ord)", l, re.I):
        print(" ", l[:220])
