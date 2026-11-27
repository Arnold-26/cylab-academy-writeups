import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = "http://xebec.cylabacademy.net:30999"
r = requests.get(base, timeout=15, verify=False)
html = r.text or ""
js = re.findall(r'src=["\']([^"\']+\.js)["\']', html)
alljs = ""
for j in js:
    rr = requests.get(base + "/" + j.lstrip("/"), timeout=15, verify=False)
    alljs += f"\n/* {j} */\n" + (rr.text or "")
inline = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S))
open(r"C:\Users\arnol\AppData\Local\Temp\cylab_bin\480_all.js", "w", encoding="utf-8").write(alljs + "\n" + inline)
print("taille js:", len(alljs), "inline:", len(inline))
for kw in ("WebSocket", "socket", "onmessage", "send(", "eval", "score", "flag", "mate"):
    for m in re.finditer(re.escape(kw), alljs + inline):
        i = m.start()
        print(f"\n--- {kw} @{i} ---")
        print((alljs + inline)[max(0, i - 150):i + 250].replace("\n", " ")[:400])
        break
