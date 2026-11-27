import sys, json, re, time, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/760/instance/?source=library")
eth = detail = None
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/760/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    if d.get("status") == "RUNNING" and desc:
        m = re.search(r"Eth node address:\s*([A-Za-z0-9.\-]+):(\d+)", desc)
        m2 = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", desc)
        if m and m2:
            eth = f"http://{m.group(1)}:{m.group(2)}"
            detail = m2.group(1)
            break
print("eth:", eth, "| detail:", detail)
if not eth:
    sys.exit(0)
info = {}
for attempt in range(6):
    try:
        r = requests.get(detail, timeout=30, verify=False)
        t = re.sub(r"<style.*?</style>", " ", r.text, flags=re.S | re.I)
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        print("=== detail page ===")
        for l in lines[:30]:
            print("  ", l[:150])
        txt = "\n".join(lines)
        mc = re.search(r"(0x[0-9a-fA-F]{40})", txt)
        mp = re.search(r"(0x[0-9a-fA-F]{64})", txt)
        if mc and mp:
            info["contract"] = mc.group(1)
            info["pk"] = mp.group(1)
        if info:
            break
    except Exception as e:
        print("essai", attempt + 1, "ERR", type(e).__name__)
        time.sleep(5)
print("\ncontract:", info.get("contract"))
print("pk:", info.get("pk"))
json.dump({"eth": eth, **info}, open(r"./_z_760info.json", "w"))
