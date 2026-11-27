# 480 - WebSockFish  (Web Exploitation, picoCTF 2025)
# Flag: academy{c1i3nt_s1d3_w3b_s0ck3t5_2327663e}
# Write-up: ../../../writeups/web-exploitation/480-websockfish.md
# Script exact utilise pour produire le flag.
#
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
open(r"/tmp/cylab_bin\480_all.js", "w", encoding="utf-8").write(alljs + "\n" + inline)
print("taille js:", len(alljs), "inline:", len(inline))
for kw in ("WebSocket", "socket", "onmessage", "send(", "eval", "score", "flag", "mate"):
    for m in re.finditer(re.escape(kw), alljs + inline):
        i = m.start()
        print(f"\n--- {kw} @{i} ---")
        print((alljs + inline)[max(0, i - 150):i + 250].replace("\n", " ")[:400])
        break
