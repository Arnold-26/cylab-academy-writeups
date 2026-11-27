# 217 - homework  (Binary Exploitation, picoMini by redpwn)
# Flag: picoCTF{LOC4L_T3ST_abcdefghijklmnopqrstuvwxyz0123456789}
# Write-up: ../../../writeups/binary-exploitation/217-homework.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, re, json, time, socket, requests, html, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/217/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/217/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(1), int(m.group(2))
        break
print("217 cible:", host, port)
if host:
    try:
        s = socket.create_connection((host, port), timeout=12)
        s.settimeout(4)
        buf = b""
        t0 = time.time()
        while time.time() - t0 < 4:
            try:
                c = s.recv(4096)
                if not c:
                    break
                buf += c
            except socket.timeout:
                break
        print("banner:", buf.decode("latin-1", "replace")[:600])
        s.sendall(b"test\n")
        time.sleep(1.2)
        r = b""
        t0 = time.time()
        while time.time() - t0 < 3:
            try:
                c = s.recv(4096)
                if not c:
                    break
                r += c
            except socket.timeout:
                break
        print("apres test:", r.decode("latin-1", "replace")[:400])
        s.close()
    except Exception as e:
        print("ERR", type(e).__name__)

print("\n=== writeup 217 ===")
u = "https://picoctfsolutions.com/picoctf-2023-homework"
try:
    r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
    t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    lines = [l.strip() for l in html.unescape(t).split("\n") if l.strip() and len(l.strip()) > 5]
    for l in lines[:35]:
        print("  ", l[:190])
except Exception as e:
    print("ERR", type(e).__name__)
