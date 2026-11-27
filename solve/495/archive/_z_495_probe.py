import requests, json, sys, time

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://chatelaine.cylabacademy.net:10774"
ME = 0xEE


def rx():
    return requests.get(BASE + "/radio_rx", timeout=15).json()


def tx(msg):
    r = requests.post(BASE + "/radio_tx", json=msg, timeout=15)
    return r.status_code


print("=== drain initial ===")
print(json.dumps(rx())[:800])
print("=== ping vers le controller (0x10) ===")
tx({"msg_type": "ping", "src": ME, "dst": 0x10})
time.sleep(0.6)
print(json.dumps(rx())[:800])
print("=== validate avec challenge 'test' ===")
tx({"msg_type": "validate", "src": ME, "dst": 0x10, "challenge": "test"})
time.sleep(0.6)
msgs = rx()
print(json.dumps(msgs)[:800])
for m in msgs:
    if m.get("msg_type") == "ack_validate":
        print("HMAC(test,0,authenticity) =", m.get("response"))
