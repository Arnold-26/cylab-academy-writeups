import sys, re, json, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()
B = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/169/instance/?source=library")
base = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/169/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", d.get("description") or "")
    if m:
        base = m.group(1)
        break
print("base:", base)
for attempt in range(4):
    try:
        files = {
            "file1": ("poeMD5_A.pdf", open(B + r"\169_poeMD5_A.pdf", "rb"), "application/pdf"),
            "file2": ("poeMD5_B.pdf", open(B + r"\169_poeMD5_B.pdf", "rb"), "application/pdf"),
        }
        r = requests.post(base + "upload", files=files, timeout=30)
        txt = re.sub(r"<[^>]+>", " ", r.text)
        txt = re.sub(r"\s+", " ", txt)
        print("upload ->", r.status_code, "|", txt[:400])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print("essai", attempt + 1, "ERR", type(e).__name__)
        time.sleep(2)
