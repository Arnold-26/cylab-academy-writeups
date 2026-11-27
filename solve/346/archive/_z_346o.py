import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/c94fc1d2fbf3153d6c7a8fd28588c1050d704f6d/picoCTF_2023/Binary_Exploitation/babygame02.md"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = html.unescape(r.text)
i = t.find("stack setup")
print(t[i:i+4500])
