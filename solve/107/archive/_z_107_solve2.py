import socket, sys, time, re, json, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_107url.txt").read().split()
port = int(port)

CHARS = string.ascii_lowercase + string.digits + "_{}" + string.ascii_uppercase + "!@#$%^&*()-+=[]:;,.?/|~` "


def connect():
    s = socket.create_connection((host, port), timeout=30)
    s.settimeout(15)
    buf = b""
    end = time.time() + 10
    while time.time() < end:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            break
        buf += d
        if b"give me: " in buf:
            break
    txt = buf.decode("latin-1")
    flag = n = e = None
    for ln in txt.split("\n"):
        if ln.startswith("flag: "):
            flag = ln[6:].strip()
        elif ln.startswith("n: "):
            n = int(ln[3:].strip())
        elif ln.startswith("e: "):
            e = int(ln[3:].strip())
    rest = txt.split("give me: ", 1)[1] if "give me: " in txt else ""
    return s, flag, n, e, rest


s, flag_ct, n, e, rest = connect()
print("n digits=%d e=%d flag digits=%d" % (len(str(n)), e, len(flag_ct)), flush=True)
buf = rest.encode("latin-1")

NQ = 0


def query(q):
    global buf, NQ
    s.sendall(q.encode("latin-1") + b"\n")
    NQ += 1
    while True:
        m = re.search(rb"Here you go: (\d+)\n", buf)
        if m:
            res = m.group(1).decode()
            buf = buf[m.end():]
            return res
        d = s.recv(65536)
        if not d:
            raise EOFError("connexion fermee apres %d requetes" % NQ)
        buf += d


flag_work = flag_ct
known = []
decrypted = ""
t0 = time.time()
while not decrypted.endswith("}"):
    found = False
    for c in CHARS:
        try:
            enc = query(decrypted + c)
        except EOFError as ex:
            print("!! ", ex, flush=True)
            print("decrypted so far:", decrypted, flush=True)
            json.dump({"decrypted": decrypted, "known": known}, open(r"./_z_107_partial.json", "w"))
            sys.exit(1)
        for k in known:
            enc = enc.replace(k, "")
        if enc and enc in flag_work:
            flag_work = flag_work.replace(enc, "", 1)
            known.append(enc)
            decrypted += c
            found = True
            print("%-40s  (%d requetes, %.0fs, bloc=%d chiffres)" % (decrypted, NQ, time.time() - t0, len(enc)), flush=True)
            break
    if not found:
        print("!! aucun caractere ne matche a la position", len(decrypted), flush=True)
        print("flag_work:", flag_work[:200])
        break
print()
print("FLAG:", decrypted)
print("requetes:", NQ)
if decrypted.endswith("}"):
    open(r"./_z_107_flag.txt", "w").write(decrypted)
s.close()
