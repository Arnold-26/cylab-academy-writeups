import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/refs/heads/main/picoCTF_2019/Forensics/m00nwalk.md"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
print(t[:2500])
print("=== flags trouves ===")
for m in re.finditer(r"picoCTF\{[^}]*\}", t):
    print(" ", m.group(0))
