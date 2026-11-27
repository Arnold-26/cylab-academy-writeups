import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%204/README.md"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = html.unescape(r.text)
print(t[:5000])
