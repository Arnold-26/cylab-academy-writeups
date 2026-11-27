import socket, sys, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"D:\ctf-index\_z_107url.txt").read().split()
port = int(port)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(2.5)

def readall(t=1.5):
    out = b""
    end = time.time() + t
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        out += d
    return out

banner = readall(3.0)
bt = banner.decode("latin-1")
flag_ct = None; n = None
for ln in bt.split("\n"):
    if ln.startswith("flag: "):
        flag_ct = ln[6:].strip()
    if ln.startswith("n: "):
        n = ln[3:].strip()
print("len(flag_ct)=", len(flag_ct), " len(n)=", len(n))
print("flag digits first/last:", flag_ct[:30], flag_ct[-30:])

def enc(s_):
    s.sendall(s_.encode() + b"\n")
    r = readall(1.5).decode("latin-1")
    m = re.search(r"Here you go: (\d+)", r)
    if not m:
        return None, r
    return m.group(1), r

for q in ["a", "b", "1", "aa", "ab", "ba", "aaa", "abc", "a"*6]:
    ct, raw = enc(q)
    print("enc(%-6r) -> len=%s %s" % (q, len(ct) if ct else None, (ct[:25] + "..." + ct[-15:]) if ct else raw[:120]))
s.close()
