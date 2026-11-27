import sys, re, json, time, requests, urllib3, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
urllib3.disable_warnings()
B = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
inv = open(B + r"\169_invite.pdf", "rb").read()
tail = inv[-1000:]
print("queue invite:", len(tail), hashlib.sha1(tail).hexdigest()[:16])
a = open(B + r"\169_shattered-1.pdf", "rb").read() + tail
b = open(B + r"\169_shattered-2.pdf", "rb").read() + tail
print("sha1 A:", hashlib.sha1(a).hexdigest())
print("sha1 B:", hashlib.sha1(b).hexdigest())
print("egaux:", hashlib.sha1(a).hexdigest() == hashlib.sha1(b).hexdigest(), "| differents:", a != b)
open(B + r"\169_craft_a.pdf", "wb").write(a)
open(B + r"\169_craft_b.pdf", "wb").write(b)

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/169/instance/?source=library")
base = None
for _ in range(10):
    time.sleep(0.8)
    st, bb = cy.req("GET", "/api/challenges/169/instance/")
    d = json.loads(bb) if bb.startswith("{") else {}
    m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", d.get("description") or "")
    if m:
        base = m.group(1)
        break
print("base:", base)
files = {
    "file1": ("a.pdf", open(B + r"\169_craft_a.pdf", "rb"), "application/pdf"),
    "file2": ("b.pdf", open(B + r"\169_craft_b.pdf", "rb"), "application/pdf"),
}
r = requests.post(base + "upload", files=files, timeout=60)
txt = re.sub(r"<[^>]+>", " ", r.text)
txt = re.sub(r"\s+", " ", txt)
print("upload ->", r.status_code, "|", txt[:300])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
print("FLAG:", m.group(0) if m else None)
