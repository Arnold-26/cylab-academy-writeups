"""495 Ricochet - step 1: MITM handshake with low-order DH point (shared = 0^32)
and test whether shared_hmac_key == authenticity_key (decrypted MAC vs validate oracle)."""
import sys, json, time
sys.path.insert(0, r".")
from _z_495_lib import *

B = sys.argv[1] if len(sys.argv) > 1 else "http://chatelaine.cylabacademy.net:40516"
r = Radio(B)
r.drain()

print("[*] state:", {k: r.state()[k] for k in ("pos", "running", "flag")})

# 1) move controller out of the way (unauthenticated set_addr)
r.tx({"msg_type": "set_addr", "src": ME, "dst": CTRL, "new_addr": 0x99})
ack = r.wait("ack_set_addr", 5)
print("[*] set_addr ack:", ack)
CTRL2 = 0x99

# 2) start
print("[*] /start ->", r.start())
v = r.wait("validate", 12)
print("[*] robot validate:", v)
ch = v["challenge"]

# 3) oracle at the controller's new address
r.tx({"msg_type": "validate", "src": ME, "dst": CTRL2, "challenge": ch})
oa = r.wait("ack_validate", 8, pred=lambda m: m.get("dst") == ME)
print("[*] oracle(robot challenge) ok:", bool(oa))
# 4) relay it to the robot
r.tx({"msg_type": "ack_validate", "src": CTRL, "dst": ROBOT, "response": oa["response"]})
print("[*] relayed ack_validate")

# 5) wait robot key_exchange, answer with low-order point
ke = r.wait("key_exchange", 12)
print("[*] robot key_exchange:", ke.get("key"))
r.tx({"msg_type": "ack_key_exchange", "src": CTRL, "dst": ROBOT, "key": bytes(32).hex()})
# also rekey the controller with the same low-order point so both sides share 0^32
r.tx({"msg_type": "key_exchange", "src": ME, "dst": CTRL2, "key": bytes(32).hex()})
time.sleep(0.3)
r.drain()

# 6) robot's first secure_data -> decrypt with shared = 0
sd = r.wait("secure_data", 12)
print("[*] secure_data:", (sd or {}).get("encrypted", "")[:40])
pt = decrypt(sd["encrypted"], bytes(32))
print("[+] DECRYPTED:", pt)

# 7) ask oracle for compute_hmac("get_movement", 0, authenticity_key)
r.tx({"msg_type": "validate", "src": ME, "dst": CTRL2, "challenge": "get_movement"})
oa2 = r.wait("ack_validate", 8, pred=lambda m: m.get("dst") == ME)
print("[*] oracle(get_movement) =", oa2["response"])
inner = json.loads(pt)
print("[*] robot mac          =", inner["hmac"])
print("=" * 60)
print("KEYS EQUAL (authenticity == shared_hmac):", oa2["response"] == inner["hmac"])
print("nonce field:", inner["nonce"], "message:", inner["message"])
