"""Toolkit for CyLab 495 "Ricochet": radio API + exact crypto (pymonocypher)."""
import requests, json, time, hashlib, monocypher

ME = 0xEE
CTRL = 0x10
ROBOT = 0x20


class Radio:
    def __init__(self, base):
        self.base = base.rstrip("/")
        self.buf = []
        self.seen = []

    def drain(self):
        try:
            msgs = requests.get(self.base + "/radio_rx", timeout=20).json()
        except Exception as e:
            msgs = []
        for m in msgs:
            self.buf.append(m)
            self.seen.append(m)
        return msgs

    def tx(self, msg):
        return requests.post(self.base + "/radio_tx", json=msg, timeout=20).status_code

    def wait(self, mtype, timeout=12.0, pred=None):
        """Wait for a message of type mtype (FIFO from buffer); returns it."""
        t0 = time.time()
        while time.time() - t0 < timeout:
            for i, m in enumerate(self.buf):
                if m.get("msg_type") == mtype and (pred is None or pred(m)):
                    return self.buf.pop(i)
            self.drain()
            time.sleep(0.05)
        return None

    def state(self):
        return requests.get(self.base + "/state", timeout=20).json()

    def start(self):
        return requests.get(self.base + "/start", timeout=20).status_code

    def stop(self):
        return requests.get(self.base + "/stop", timeout=20).status_code


# ---------- crypto (mirror of crypto.py) ----------
B2 = lambda x: monocypher.blake2b(x)


def compute_hmac(message, nonce, key):
    h = (message + str(nonce) + key.hex()).encode()
    for _ in range(32):
        h = monocypher.blake2b(h + key)
    return monocypher.blake2b(h)


def add_hmac(message, nonce, key, mac=None):
    if mac is None:
        mac = compute_hmac(message, nonce, key)
    return {"message": message, "nonce": nonce, "hmac": mac.hex()}


def encrypt(message, dhkey):
    key = B2(dhkey)[:32]
    import os
    nonce = os.urandom(24)
    tag, ct = monocypher.lock(key, nonce, message.encode() if isinstance(message, str) else message)
    return ct.hex() + ";" + tag.hex() + ";" + nonce.hex()


def decrypt(blob, dhkey):
    key = B2(dhkey)[:32]
    ct, tag, nonce = blob.split(";")
    pt = monocypher.unlock(key, bytes.fromhex(nonce), bytes.fromhex(tag), bytes.fromhex(ct))
    if pt is None:
        return None
    return bytes(pt).decode()


ZERO = bytes(32)
ZKEY = None
