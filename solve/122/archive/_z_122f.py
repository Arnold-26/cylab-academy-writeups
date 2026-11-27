import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://pugachev.io/2023/12/22/easy-as-gdb-by-picoctf/"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip()]
start = 0
for i, l in enumerate(lines):
    if "xor with constants" in l:
        start = i
        break
for l in lines[start:start + 70]:
    print(l[:200])
