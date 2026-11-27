import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://picoctf2021.haydenhousen.com/cryptography/it-is-my-birthday-2.md"
try:
    r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
    t = html.unescape(r.text)
    print(t[:3000])
except Exception as e:
    print("ERR", type(e).__name__)
