#!/usr/bin/env python3
# 495 - Ricochet  (Cryptography, picoCTF 2022)
# Flag: academy{r1gh7_84ck_47_y4_38227532}
# Write-up: ../../../writeups/cryptography/495-ricochet.md
# This is the script that produced the flag; historical variants are in archive/.
#
"""495 Ricochet : exploit one-shot.

La table de MAC (_z_495_macs.json) est statique d'une instance a l'autre (la cle du
serveur est fixe), il suffit donc de :
  * faire quelques passes d'oracle pour obtenir les MAC des directions aux nonces voulus
    (le controller du robot est un oracle de MAC pour "", east, south, west, north),
  * puis usurper le controller et injecter tout le dialogue d'un coup dans le buffer de
    reception du robot (wait_message ne verifie pas src).

Usage : python3 solve.py <host> <port>
Dependances : _z_495_atk.py, _z_495_lib.py, _z_495_macs.json (dans ce dossier)
"""
import sys, json, time
sys.path.insert(0, r".")
import _z_495_atk as A
from _z_495_lib import *

Z = bytes(32)
PATH = ["east", "south", "east", "north", "west",
        "south", "east", "north", "east", "south"]
P2 = {i: "empty" for i in (0, 2, 4, 6, 8, 10)}              # -> east @1..13
P3 = {0: "empty", 2: "empty", 4: "gm", 6: "gm", 8: "gm"}   # -> west @9


def blast(r, plan, length, ctlf=0x99):
    A.TBL  # noqa
    for i in range(length):
        if i % 2 == 0:
            kind = plan.get(i, "gm")
            msg = "get_movement" if kind == "gm" else ""
            tx = "secure_data"
        else:
            msg, tx = "", "secure_data_request"
        r.tx({"msg_type": tx, "src": ME, "dst": ctlf, "encrypted": A.enc(msg, i)})
    t0 = time.time()
    while time.time() - t0 < 4:
        A.drain(r)
        time.sleep(0.05)


def pass_(r, plan, length, need):
    r.stop(); time.sleep(0.3)
    r.drain(); r.ctrl = CTRL
    A.set_ctrl(r, 0x99)
    r.start()
    v = r.wait("validate", 12)
    if not v:
        print("  !! no validate"); return False
    r.tx({"msg_type": "ack_validate", "src": CTRL, "dst": ROBOT, "response": "00" * 64})
    # rekey controller to the all-zero low order point -> we know its key
    r.tx({"msg_type": "key_exchange", "src": ME, "dst": 0x99, "key": Z.hex()})
    time.sleep(0.25)
    blast(r, plan, length)
    got = [(k, k in A.TBL) for k in need]
    print("   pass ->", got, flush=True)
    return all(x[1] for x in got)


def serve(r, cmds):
    r.stop(); time.sleep(0.3)
    r.drain(); r.ctrl = CTRL
    A.set_ctrl(r, 0x99)
    r.start()
    if A.handshake(r, 0x99) is None:
        print("  !! handshake failed"); return None
    print("[C] handshake OK, blasting dialogue", flush=True)
    n = 0
    for k, c in enumerate(cmds):
        r.tx({"msg_type": "secure_data_ack", "src": CTRL, "dst": ROBOT,
              "encrypted": A.enc("", n)})
        r.tx({"msg_type": "secure_data_response", "src": CTRL, "dst": ROBOT,
              "encrypted": A.enc(c, n + 1)})
        n += 2
    print("[C] blasted", n, "messages", flush=True)
    for _ in range(6):
        time.sleep(1.0)
        s = r.state()
        print("   POS", s["pos"], "| FLAG:", s["flag"], flush=True)
        if "has not yet" not in s["flag"]:
            break
    s = r.state()
    print("[C] FINAL POS", s["pos"], "| FLAG:", s["flag"])
    for l in s["log"][:16]:
        print("   ", l)
    return s


def main():
    url = A.launch()
    print("[*] instance:", url, flush=True)
    if not url:
        return
    r = Radio(url); r.ctrl = CTRL
    need = [("east", 1), ("south", 3), ("east", 5), ("north", 7),
            ("west", 9), ("south", 11), ("east", 13), ("north", 15),
            ("east", 17), ("south", 19)]
    missing = [k for k in need if k not in A.TBL]
    print("[*] missing before passes:", missing, flush=True)
    if any(k[0] == "east" and k[1] in (5, 13) for k in missing):
        pass_(r, P2, 14, [k for k in missing if k[0] == "east"])
    if ("west", 9) in [k for k in need if k not in A.TBL]:
        pass_(r, P3, 10, [("west", 9)])
    A.save()
    print("[*] missing after passes:", [k for k in need if k not in A.TBL], flush=True)
    serve(r, PATH)


if __name__ == "__main__":
    main()
