import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picoctf-2023-unforgottenbits",
                 timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 12]
for i, l in enumerate(lines):
    if re.search(r"(flag|steghide|openssl|aes|bmp|akali|gallery|hidden|decrypt)", l, re.I):
        print("%3d| %s" % (i, l[:200]))
