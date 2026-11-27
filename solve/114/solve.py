# 114 - Play Nice  (Cryptography, picoCTF 2021)
# Flag: not archived
# Write-up: ../../../writeups/cryptography/114-play-nice.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, re, json, time, socket

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SIZE = 6


def make_matrix(alphabet):
    m = []
    for i, ch in enumerate(alphabet):
        if i % SIZE == 0:
            row = []
        row.append(ch)
        if i % SIZE == SIZE - 1:
            m.append(row)
    return m


def decrypt_pair(pair, m):
    idx = {}
    for r in range(SIZE):
        for c in range(SIZE):
            idx[m[r][c]] = (r, c)
    p1 = idx[pair[0]]
    p2 = idx[pair[1]]
    if p1[0] == p2[0]:
        return m[p1[0]][(p1[1] - 1) % SIZE] + m[p2[0]][(p2[1] - 1) % SIZE]
    if p1[1] == p2[1]:
        return m[(p1[0] - 1) % SIZE][p1[1]] + m[(p2[0] - 1) % SIZE][p2[1]]
    return m[p1[0]][p2[1]] + m[p2[0]][p1[1]]


host = port = None
for _ in range(10):
    time.sleep(1)
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(8)
buf = b""
t0 = time.time()
while b"plaintext" not in buf and time.time() - t0 < 8:
    try:
        c = s.recv(4096)
        if not c:
            break
        buf += c
    except socket.timeout:
        break
txt = buf.decode("latin-1", "replace")
print(txt[:400])
al = re.search(r"alphabet:\s*(\S+)", txt).group(1)
ct = re.search(r"encrypted message:\s*(\S+)", txt).group(1)
print("alphabet:", al[:20], "... len", len(al))
print("cipher:", ct)
mat = make_matrix(al)
pt = "".join(decrypt_pair(ct[i:i + 2], mat) for i in range(0, len(ct), 2))
print("plaintext:", repr(pt))
for cand in (pt, pt[:-1] if pt.endswith("{") else pt):
    s.sendall(cand.encode() + b"\n")
    time.sleep(0.4)
    out = b""
    t0 = time.time()
    while time.time() - t0 < 4:
        try:
            cc = s.recv(4096)
            if not cc:
                break
            out += cc
        except socket.timeout:
            break
    o = out.decode("latin-1", "replace")
    print("envoi %r -> %s" % (cand[-8:], o[:300]))
    mflag = re.search(r"(?:academy|picoCTF)\{[^}]*\}", o)
    if mflag:
        print("FLAG:", mflag.group(0))
        break
s.close()
