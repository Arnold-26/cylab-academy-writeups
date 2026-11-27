import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://picoctfsolutions.com/picoctf-2019-investigation-encoded-1",
                 timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip()]
for i, l in enumerate(lines):
    if re.search(r"(flag|picoCTF\{|academy\{|decod|matrix|secret)", l, re.I) and len(l) > 10:
        print("%3d| %s" % (i, l[:200]))
