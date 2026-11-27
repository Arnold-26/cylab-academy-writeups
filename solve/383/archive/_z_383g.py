import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Forensics/UnforgottenBits/UnforgottenBits.md"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = html.unescape(r.text)
print("=== toutes les occurrences de picoCTF{ / academy{ ===")
for m in re.finditer(r"(?:picoCTF|academy)\{[^}\n]{3,120}\}", t):
    print(" ", m.group(0))
print()
idx = t.find("f473")
print("=== contexte autour de f473 ===")
print(t[max(0, idx-600):idx+600])
