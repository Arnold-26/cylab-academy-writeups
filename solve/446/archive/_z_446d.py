import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

# sequence : w*4 -> (0,4) ; a*11 -> (0,-7) ; d*3 -> (0,-4) ; d*4 -> (0,0) ; s*29 -> (29,0) ; d*89 -> (29,89)
seq = "w" * 4 + "a" * 11 + "d" * 3 + "d" * 4 + "s" * 29 + "d" * 89
print("longueur sequence:", len(seq))

def run(sock, data):
    sock.sendall(data.encode() + b"\n")
    time.sleep(3)
    out = b""
    try:
        while True:
            c = sock.recv(65536)
            if not c:
                break
            out += c
    except Exception:
        pass
    return out

# test local d'abord
import subprocess
p = subprocess.run(["./446_game"], input=seq + "\n", capture_output=True, text=True,
                   cwd="/tmp/cylab_eps/t446", timeout=30)
print("=== LOCAL (fin) ===")
print(p.stdout[-800:])
