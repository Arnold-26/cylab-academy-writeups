import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/refs/heads/main/General%20Skills/YaraRules0x100.md"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
print("HTTP", r.status_code, len(r.text))
print(r.text[:3000])
