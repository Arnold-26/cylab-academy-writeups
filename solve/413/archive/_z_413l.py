import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://omar-4.gitbook.io/omar-khalid/pages/ctf-writeups/forensics-challenge-dear-diary-or-picoctf-writeup"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = html.unescape(t)
lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 3]
start = 0
for i, l in enumerate(lines):
    if "Interpreting the Clues" in l:
        start = i
        break
for l in lines[start:start + 60]:
    print("  ", l[:200])
print("=== flags ===")
for m in re.finditer(r"(?:picoCTF|academy)\{[^}]*\}", t):
    print(" ", m.group(0))
