import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Forensics/UnforgottenBits/UnforgottenBits.md"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = html.unescape(r.text)
lines = [l.strip() for l in t.split("\n") if l.strip()]
print("total lignes:", len(lines))
start = 0
for i, l in enumerate(lines):
    if "7.bmp" in l or "7\.bmp" in l:
        start = max(0, i - 5)
        break
for l in lines[start:start + 70]:
    if l.startswith("!["):
        continue
    print("  ", l[:190])
print("=== flags ===")
for m in re.finditer(r"(?:picoCTF|academy)\{[^}]*\}", t):
    print(" ", m.group(0))
