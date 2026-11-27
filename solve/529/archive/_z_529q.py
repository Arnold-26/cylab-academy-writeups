import sys, requests, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = open(r"./_z_529base.txt").read().strip()
print("base:", base)
for path in ("/verify-otp", "/", "/download/"):
    try:
        r = requests.get(base + path, timeout=15, verify=False)
        print("GET %-14s -> %s %r" % (path, r.status_code, r.text[:150]))
    except Exception as e:
        print("GET", path, "ERR", type(e).__name__)
print()
for otp in ("0000", "1234", "1111"):
    try:
        r = requests.post(base + "/verify-otp", json={"otp": otp}, timeout=15, verify=False)
        print("POST otp=%-6s -> %s %r" % (otp, r.status_code, r.text[:300]))
    except Exception as e:
        print("POST", otp, "ERR", type(e).__name__)
# variante form
try:
    r = requests.post(base + "/verify-otp", data={"otp": "1234"}, timeout=15, verify=False)
    print("POST form ->", r.status_code, r.text[:300])
except Exception as e:
    print("POST form ERR", type(e).__name__)
