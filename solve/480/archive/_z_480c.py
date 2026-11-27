import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = "http://xebec.cylabacademy.net:30999"
r = requests.get(base, timeout=15, verify=False)
html = r.text or ""
inline = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S))
print(inline)
