import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://7rocky.github.io/en/ctf/picoctf/binary-exploitation/bizz-fuzz/",
                 timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.rstrip() for l in t.split("\n")]
# chercher les sections interessantes
for i, l in enumerate(lines):
    if re.search(r"(fizzbuzz|recvuntil|sendline|payload|0x8049206|0x808ba|Opening way|vulnerable)", l, re.I):
        print("%3d| %s" % (i, l[:170]))
