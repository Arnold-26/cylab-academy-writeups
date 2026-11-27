import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:27114/"
t = requests.get(BASE + "designer.js", timeout=20).text
for m in re.finditer(r"['\"`](/api[^'\"`]*|/[a-z0-9_/-]+)['\"`]", t):
    print("  endpoint:", m.group(1))
print("=== extraits autour de fetch/axios ===")
for m in re.finditer(r".{80}(fetch|XMLHttpRequest|axios).{160}", t, re.S):
    print("  ...", re.sub(r"\s+", " ", m.group(0))[:220])
