"""495 Ricochet - one-shot attack driver.

phase A: MITM handshake w/ low-order DH point (shared=0^32) -> capture legit run MAC table
phase B: use the controller as a MAC oracle to collect direction MACs at chosen nonces
phase C: impersonate the controller, feed the robot the slide sequence, land on the flag
"""
import sys, json, time, os, re
sys.path.insert(0, r"D:\ctf-index")
from _z_495_lib import *

Z = bytes(32)
TBLF = r"D:\ctf-index\_z_495_macs.json"
TBL = {}
if os.path.exists(TBLF):
    TBL = {tuple(json.loads(k)): v for k, v in json.load(open(TBLF)).items()}


def save():
    json.dump({json.dumps(list(k)): v for k, v in TBL.items()}, open(TBLF, "w"))


def put(msg, nonce, hmac):
    k = (msg, nonce)
    if k in TBL and TBL[k] != hmac:
        print("  !! MAC CONFLICT", k)
    TBL[k] = hmac


def enc(msg, nonce):
    b = {"message": msg, "nonce": nonce, "hmac": TBL[(msg, nonce)]}
    return encrypt(json.dumps(b), Z)


SEC = ("secure_data", "secure_data_ack", "secure_data_request", "secure_data_response")


def drain(r, verbose=False):
    n = 0
    for m in r.drain():
        if m.get("msg_type") not in SEC:
            continue
        try:
            pt = json.loads(decrypt(m["encrypted"], Z))
        except Exception as e:
            if verbose: print("   !! undecryptable", m.get("msg_type"), repr(e)[:50])
            continue
        put(pt["message"], pt["nonce"], pt["hmac"])
        n += 1
        if verbose:
            print("   %-21s nonce=%-3s msg=%r" % (m.get("msg_type"), pt["nonce"], pt["message"]))
    return n


def harvest(r, seconds):
    t0 = time.time()
    while time.time() - t0 < seconds:
        drain(r)
        time.sleep(0.03)


def set_ctrl(r, new):
    for _ in range(3):
        r.tx({"msg_type": "set_addr", "src": ME, "dst": r.ctrl, "new_addr": new})
        a = r.wait("ack_set_addr", 5)
        if a:
            r.ctrl = new
            return True
    return False


def handshake(r, ctrl_dst, bogus=False, restore_to=None):
    """Relay validate via the oracle, then rekey both ends to the all-zero DH point.
    The robot waits up to 10s for ack_key_exchange, which gives us time to move the
    controller back into place before the robot's first secure_data."""
    v = r.wait("validate", 15)
    if not v:
        print("  !! no validate from robot"); return None
    ch = v["challenge"]
    if bogus:
        r.tx({"msg_type": "ack_validate", "src": CTRL, "dst": ROBOT, "response": "00" * 64})
        return ch
    r.tx({"msg_type": "validate", "src": ME, "dst": ctrl_dst, "challenge": ch})
    oa = r.wait("ack_validate", 8, pred=lambda m: m.get("dst") == ME)
    if not oa:
        print("  !! oracle failed"); return None
    r.tx({"msg_type": "ack_validate", "src": CTRL, "dst": ROBOT, "response": oa["response"]})
    ke = r.wait("key_exchange", 12)
    if not ke:
        print("  !! no key_exchange"); return None
    # rekey the controller with the low-order point (it ignores the robot's key: it is away)
    r.tx({"msg_type": "key_exchange", "src": ME, "dst": ctrl_dst, "key": Z.hex()})
    time.sleep(0.25)
    if restore_to is not None:
        set_ctrl(r, restore_to)
        time.sleep(0.15)
    # now release the robot
    r.tx({"msg_type": "ack_key_exchange", "src": CTRL, "dst": ROBOT, "key": Z.hex()})
    return ch


def phaseA(r):
    r.drain(); r.ctrl = CTRL
    set_ctrl(r, 0x99)
    r.stop(); time.sleep(0.4)
    r.start()
    if not handshake(r, 0x99, restore_to=CTRL): return False
    print("[A] capturing legit run (shared key 0^32)...")
    t0 = time.time()
    while time.time() - t0 < 28:
        drain(r, verbose=True)
        time.sleep(0.03)
    save()
    print("[A] table:", len(TBL))
    return True


def expect(r, nonce, timeout=2.5):
    """wait until the table has some entry with this nonce (any message)"""
    t0 = time.time()
    while time.time() - t0 < timeout:
        drain(r)
        if any(k[1] == nonce for k in TBL):
            return True
        time.sleep(0.03)
    return False


def phaseB(r, plan, length, ctlf=0x99):
    r.stop(); time.sleep(0.4)
    r.drain(); r.ctrl = CTRL
    set_ctrl(r, ctlf)
    r.start()
    if handshake(r, ctlf, bogus=True) is None: return False
    time.sleep(0.15)
    ok = 0
    for i in range(length):
        if i % 2 == 0:
            kind = plan.get(i, "gm")
            msg = "get_movement" if kind == "gm" else ""
            tx = "secure_data"
        else:
            msg, tx = "", "secure_data_request"
        if (msg, i) not in TBL:
            print("  !! missing MAC", (msg, i)); return False
        n0 = sum(1 for k in TBL if k[1] == i)
        r.tx({"msg_type": tx, "src": ME, "dst": ctlf, "encrypted": enc(msg, i)})
        t0 = time.time(); got = False
        while time.time() - t0 < 2.0:
            drain(r)
            if sum(1 for k in TBL if k[1] == i) > n0:
                got = True; break
            time.sleep(0.03)
        if not got:
            print("  !! no response at nonce", i, "(controller nonce mismatch?)")
            return False
        ok += 1
    print("  pass ok (%d msg), table %d" % (ok, len(TBL)))
    return True


def find_ctrl_nonce(r, ctlf):
    """probe which nonce the controller expects (needs MAC('',k) in table)"""
    for k in range(0, 46):
        if ("", k) not in TBL:
            continue
        r.tx({"msg_type": "secure_data_request", "src": ME, "dst": ctlf, "encrypted": enc("", k)})
        t0 = time.time()
        while time.time() - t0 < 0.8:
            for m in r.drain():
                if m.get("msg_type") == "secure_data_response":
                    try: pt = json.loads(decrypt(m["encrypted"], Z))
                    except Exception: continue
                    put(pt["message"], pt["nonce"], pt["hmac"])
                    if pt["nonce"] == k:
                        print("[?] controller nonce =", k)
                        return k + 1
            time.sleep(0.03)
    return None


def phaseC(r, cmds):
    r.stop(); time.sleep(0.4)
    r.drain(); r.ctrl = CTRL
    set_ctrl(r, 0x99)
    r.start()
    if handshake(r, 0x99) is None: return
    print("[C] handshake done; serving", len(cmds), "commands")
    k = 0
    deadline = time.time() + 120
    while time.time() < deadline and k < len(cmds):
        for m in r.drain():
            t = m.get("msg_type")
            if t not in ("secure_data", "secure_data_request"):
                continue
            try:
                pt = json.loads(decrypt(m["encrypted"], Z))
            except Exception:
                continue
            n = pt["nonce"]
            if t == "secure_data":
                if ("", n) not in TBL:
                    print("  !! no ack MAC", n); return
                r.tx({"msg_type": "secure_data_ack", "src": CTRL, "dst": ROBOT,
                      "encrypted": enc("", n)})
                print("   ack @%d (%r)" % (n, pt["message"]))
            else:
                cmd = cmds[k] if k < len(cmds) else ""
                if (cmd, n) not in TBL:
                    print("  !! no MAC for %r @%d" % (cmd, n)); return
                r.tx({"msg_type": "secure_data_response", "src": CTRL, "dst": ROBOT,
                      "encrypted": enc(cmd, n)})
                print("   cmd[%d] %-5s @%d" % (k, cmd, n))
                if k < len(cmds):
                    k += 1
        time.sleep(0.03)
    print("[C] sent", k, "/", len(cmds))
    time.sleep(2.0)
    s = r.state()
    print("[C] POS", s["pos"], "| FLAG:", s["flag"])
    for l in s["log"][:12]:
        print("   ", l)
    return s


def launch():
    from cylab2 import CyLab
    cy = CyLab(delay=1.5)
    cy.login()
    cy.req("PUT", "/api/challenges/495/instance/?source=library")
    for _ in range(8):
        time.sleep(2)
        st, b = cy.req("GET", "/api/challenges/495/instance/")
        try:
            d = json.loads(b)
        except Exception:
            continue
        if d.get("status") == "RUNNING":
            m = re.search(r"http://[^\s'\"<>]+", d.get("description") or "")
            if m:
                return m.group(0)
    return None


PLAN1 = {}                                   # all in-phase: natural cycle
PLAN2 = {i: "empty" for i in range(0, 13, 2)}  # all east up to nonce 13
PLAN3 = {0: "empty", 2: "empty", 4: "gm", 6: "gm", 8: "gm"} | {i: "empty" for i in range(10, 20, 2)}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "go"
    if mode == "go":
        url = launch()
        print("[*] instance:", url)
        if not url: sys.exit(1)
        r = Radio(url); r.ctrl = CTRL
        if not phaseA(r):
            print("!! phase A failed"); sys.exit(1)
        print("[B] pass1 (natural cycle)")
        phaseB(r, PLAN1, 20)
        print("[B] pass2 (all east)")
        phaseB(r, PLAN2, 20)
        print("[B] pass3 (west @9)")
        phaseB(r, PLAN3, 12)
        save()
        print("[B] table:", len(TBL))
        for k in sorted(TBL):
            if k[1] < 21: print("   ", k, TBL[k][:12])
        cmds = "east,south,east,north,west,south,east,north,east,south".split(",")
        phaseC(r, cmds)
    else:
        url = sys.argv[2]
        r = Radio(url); r.ctrl = CTRL
        phaseC(r, sys.argv[3].split(","))
