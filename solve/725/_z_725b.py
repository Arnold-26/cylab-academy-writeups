import sys, json, re, time, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.8)
cy.login()
st, b = cy.req("GET", "/api/challenges/725/instance/")
d = json.loads(b)
print("=== DESC COMPLETE ===")
print(d.get("description"))
# writeup
try:
    r = requests.get("https://picoctfsolutions.com/picoctf-2026-north-south", timeout=30, verify=False)
    t = re.sub(r"<script.*?</script>", " ", r.text, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 25]
    print("\n=== WRITEUP (technique) ===")
    for l in lines:
        if re.search(r"(header|geo|X-Forwarded|X-Real|region|country|nginx|proxy|curl|curl -H|spoof)", l, re.I):
            print("  ", l[:200])
except Exception as e:
    print("writeup ERR", type(e).__name__)
