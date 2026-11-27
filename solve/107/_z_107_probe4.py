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

bt = readall(3.0).decode("latin-1")
flag_ct = n = e = None
for ln in bt.split("\n"):
    if ln.startswith("flag: "):
        flag_ct = ln[6:].strip()
    elif ln.startswith("n: "):
        n = int(ln[3:].strip())
    elif ln.startswith("e: "):
        e = int(ln[3:].strip())
print("len(flag_ct)=%d len(n)=%d e=%d" % (len(flag_ct), len(str(n)), e))

def enc(q):
    s.sendall(q.encode() + b"\n")
    r = readall(1.5).decode("latin-1")
    m = re.search(r"Here you go: (\d+)", r)
    return m.group(1) if m else None

tbl = {}
for q in ["a", "b", "1", "aa", "ab", "ba", "academy{"]:
    ct = enc(q)
    tbl[q] = ct
    print("enc(%r) len=%d" % (q, len(ct)))

# verification RSA textbook
print()
print("pow(97,e,n) len:", len(str(pow(ord('a'), e, n))), " == enc('a') ?", str(pow(ord('a'), e, n)) == tbl['a'])
print("pow(98,e,n)  == enc('b') ?", str(pow(ord('b'), e, n)) == tbl['b'])
print("pow(49,e,n)  == enc('1') ?", str(pow(ord('1'), e, n)) == tbl['1'])
print()
print("enc('aa') == a||a ?", tbl['aa'] == tbl['a'] + tbl['a'])
print("enc('ab') == a||b ?", tbl['ab'] == tbl['a'] + tbl['b'])
print("enc('ab') == b||a ?", tbl['ab'] == tbl['b'] + tbl['a'])
print("enc('ba') == a||b ?", tbl['ba'] == tbl['a'] + tbl['b'])
print("enc('ba') == b||a ?", tbl['ba'] == tbl['b'] + tbl['a'])
print()
print("enc('academy{') prefix tests:")
t = tbl['academy{']
print("  startswith enc('a')?", t.startswith(tbl['a']))
print("  startswith enc('ac')?", t[:len(enc('ac'))] if False else '-')
print("  len:", len(t))
open(r"D:\ctf-index\_z_107_data1.txt", "w").write("%s\n%d\n%d\n" % (flag_ct, n, e))
import json
json.dump({"flag_ct": flag_ct, "n": str(n), "e": e, "tbl": tbl}, open(r"D:\ctf-index\_z_107_data1.json", "w"))
s.close()
