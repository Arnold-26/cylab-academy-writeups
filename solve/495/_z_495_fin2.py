"""495 Ricochet - finishing move: one oracle pass for east@5, then serve the dialogue."""
import sys, json, time
sys.path.insert(0, r".")
import _z_495_atk as A
from _z_495_lib import *

Z = bytes(32)
PATH = ["east", "south", "east", "north", "west",
        "south", "east", "north", "east", "south"]
NEED = [("east", 1), ("south", 3), ("east", 5), ("north", 7), ("west", 9),
        ("south", 11), ("east", 13), ("north", 15), ("east", 17), ("south", 19)]


def fresh(r):
    r.drain(); r.buf.clear()


def pass_(r, plan, length, need):
    r.stop(); time.sleep(0.3)
    fresh(r); r.ctrl = CTRL
    A.set_ctrl(r, 0x99)
    fresh(r)
    r.start()
    v = r.wait("validate", 12)
    if not v:
        print("  !! no validate"); return False
    print("  validate ch", v["challenge"])
    r.tx({"msg_type": "ack_validate", "src": CTRL, "dst": ROBOT, "response": "00" * 64})
    r.tx({"msg_type": "key_exchange", "src": ME, "dst": 0x99, "key": Z.hex()})
    time.sleep(0.3)
    for i in range(length):
        if i % 2 == 0:
            msg = "get_movement" if plan.get(i, "gm") == "gm" else ""
            tx = "secure_data"
        else:
            msg, tx = "", "secure_data_request"
        r.tx({"msg_type": tx, "src": ME, "dst": 0x99, "encrypted": A.enc(msg, i)})
    t0 = time.time()
    while time.time() - t0 < 4:
        A.drain(r); time.sleep(0.05)
    print("   pass ->", [(k, k in A.TBL) for k in need], flush=True)
    return all(k in A.TBL for k in need)


def serve(r, cmds):
    r.stop(); time.sleep(0.3)
    fresh(r); r.ctrl = CTRL
    A.set_ctrl(r, 0x99)
    fresh(r)
    r.start()
    for attempt in (1, 2):
        v = r.wait("validate", 12)
        if not v:
            print("  !! no validate (attempt %d)" % attempt); continue
        ch = v["challenge"]
        print("[C] robot challenge", ch)
        r.tx({"msg_type": "validate", "src": ME, "dst": 0x99, "challenge": ch})
        oa = r.wait("ack_validate", 8, pred=lambda m: m.get("dst") == ME)
        if not oa:
            print("  !! oracle failed"); continue
        r.tx({"msg_type": "ack_validate", "src": CTRL, "dst": ROBOT,
              "response": oa["response"]})
        ke = r.wait("key_exchange", 8)
        if not ke:
            print("  !! no key_exchange (attempt %d)" % attempt); continue
        print("[C] key_exchange seen, releasing robot")
        r.tx({"msg_type": "ack_key_exchange", "src": CTRL, "dst": ROBOT, "key": Z.hex()})
        break
    else:
        return None
    n = 0
    for k, c in enumerate(cmds):
        r.tx({"msg_type": "secure_data_ack", "src": CTRL, "dst": ROBOT,
              "encrypted": A.enc("", n)})
        r.tx({"msg_type": "secure_data_response", "src": CTRL, "dst": ROBOT,
              "encrypted": A.enc(c, n + 1)})
        n += 2
    print("[C] blasted", n, "messages", flush=True)
    for _ in range(8):
        time.sleep(1.2)
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
    if ("east", 5) not in A.TBL:
        pass_(r, {0: "empty", 2: "empty"}, 6, [("east", 5)])
        A.save()
    miss = [k for k in NEED if k not in A.TBL]
    print("[*] missing:", miss, flush=True)
    serve(r, PATH)


if __name__ == "__main__":
    main()
