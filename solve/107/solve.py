# 107 - Scrambled: RSA  (Cryptography, picoCTF 2021)
# Flag: academy{bad_1d3a5_73efa9c}
# Write-up: ../../../writeups/cryptography/107-scrambled-rsa.md
# Script exact utilise pour produire le flag.
#
import socket, sys, time, re, json, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_107url.txt").read().split()
port = int(port)

KNOWN_PREFIX = "academy{bad_1d3a5"
CHARS = (string.ascii_lowercase + string.digits + "_}{" +
         string.ascii_uppercase + "!@#$%^&*()-+=[]:;,./?|~`")


class Conn:
    def __init__(self):
        self.s = socket.create_connection((host, port), timeout=30)
        self.s.settimeout(10)
        self.buf = b""
        self.nq = 0
        txt = self._banner()
        self.flag = self.n = self.e = None
        for ln in txt.split("\n"):
            if ln.startswith("flag: "):
                self.flag = ln[6:].strip()
            elif ln.startswith("n: "):
                self.n = int(ln[3:].strip())
            elif ln.startswith("e: "):
                self.e = int(ln[3:].strip())
        self.work = self.flag
        self.known = []
        self.plain = ""

    def _banner(self):
        out = b""
        end = time.time() + 12
        while time.time() < end:
            try:
                d = self.s.recv(65536)
            except socket.timeout:
                break
            if not d:
                break
            out += d
            if b"give me: " in out:
                break
        if b"give me: " in out:
            head, tail = out.split(b"give me: ", 1)
            self.buf = tail
            return head.decode("latin-1")
        self.buf = b""
        return out.decode("latin-1")

    def query(self, q, retries=4):
        for att in range(retries):
            self.s.sendall(q.encode("latin-1") + b"\n")
            self.nq += 1
            end = time.time() + 12
            while time.time() < end:
                m = re.search(rb"Here you go: (\d+)\n", self.buf)
                if m:
                    res = m.group(1).decode()
                    self.buf = self.buf[m.end():]
                    return res
                try:
                    d = self.s.recv(65536)
                except socket.timeout:
                    break
                if not d:
                    raise EOFError("closed")
                self.buf += d
            print("   (timeout, retry %d)" % att, flush=True)
        raise EOFError("timeout x%d" % retries)


def main():
    c = Conn()
    print("flag=%d chiffres, n=%d chiffres, e=%d" % (len(c.flag), len(str(c.n)), c.e), flush=True)
    t0 = time.time()
    # 1) etablir les blocs du prefixe connu
    for i in range(len(KNOWN_PREFIX)):
        prefix = KNOWN_PREFIX[:i + 1]
        enc = c.query(prefix)
        for k in c.known:
            enc = enc.replace(k, "")
        if not enc:
            print("!! bloc introuvable pour la position", i, flush=True)
            return
        c.known.append(enc)
        c.work = c.work.replace(enc, "", 1)
        c.plain = prefix
        print("prefixe %-30s bloc=%d (work reste %d chiffres)" % (prefix, len(enc), len(c.work)), flush=True)
    # 2) chercher la suite
    while not c.plain.endswith("}"):
        found = False
        for ch in CHARS:
            try:
                enc = c.query(c.plain + ch)
            except EOFError as ex:
                print("!! %r apres %d requetes ; plain=%r" % (ex, c.nq, c.plain), flush=True)
                json.dump({"plain": c.plain}, open(r"./_z_107_partial.json", "w"))
                return
            for k in c.known:
                enc = enc.replace(k, "")
            if enc and enc in c.work:
                c.work = c.work.replace(enc, "", 1)
                c.known.append(enc)
                c.plain += ch
                found = True
                print("%-45s (%d req, %.0fs)" % (c.plain, c.nq, time.time() - t0), flush=True)
                break
        if not found:
            print("!! aucun candidat a la position %d ; work=%r" % (len(c.plain), c.work[:120]), flush=True)
            break
    print()
    print("FLAG:", c.plain)
    print("requetes:", c.nq, "temps: %.0fs" % (time.time() - t0))
    if c.plain.endswith("}"):
        open(r"./_z_107_flag.txt", "w").write(c.plain)


main()
