import sys, re, json, time, socket, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.3)
cy.login()
cy.req("PUT", "/api/challenges/107/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/107/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(1), int(m.group(2))
        break
print("cible:", host, port)
alpha = string.ascii_lowercase + string.digits + "_" + string.ascii_uppercase + "{}!-@#"
s = socket.create_connection((host, port), timeout=20)
s.settimeout(3)
banner = b""
t0 = time.time()
while time.time() - t0 < 3:
    try:
        c = s.recv(65536)
        if not c:
            break
        banner += c
        if b"give me" in banner:
            break
    except socket.timeout:
        break
txt = banner.decode("latin-1", "replace")
flagnum = re.search(r"flag:\s*(\d+)", txt).group(1)
print("flag digits:", len(flagnum))
codebook = {}
for ch in alpha:
    s.sendall(ch.encode() + b"\n")
    time.sleep(0.25)
    r = b""
    t0 = time.time()
    while time.time() - t0 < 1.5:
        try:
            c = s.recv(65536)
            if not c:
                break
            r += c
        except socket.timeout:
            break
    m = re.search(rb"(\d{20,})", r)
    if m:
        codebook[ch] = m.group(1).decode()
s.close()
print("codebook:", len(codebook))
lens = sorted(set(len(v) for v in codebook.values()))
print("longueurs des chiffres:", lens[:6], "...", lens[-3:])
# parcours glouton du nombre du flag
pos = 0
out = []
while pos < len(flagnum) and len(out) < 80:
    matched = False
    for ch, code in sorted(codebook.items(), key=lambda kv: -len(kv[1])):
        if flagnum.startswith(code, pos):
            out.append(ch)
            pos += len(code)
            matched = True
            break
    if not matched:
        break
res = "".join(out)
print("reconstruit:", res)
print("reste a partir de", pos, ":", flagnum[pos:pos + 40])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", res)
print("FLAG:", m.group(0) if m else None)
