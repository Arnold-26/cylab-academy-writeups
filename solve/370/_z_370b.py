import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 20763
WARRIOR = """;redcode-94
;name Herem/Scimitar
;author aCa
;strategy bomber tuned versus the Imp
bomb       dat #4, #4
start      add.ab #4, bomb
           mov.i   bomb, @bomb
           jmp     start
end start
"""
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(10)
time.sleep(0.5)
out = b""
try:
    out = s.recv(8192)
except Exception:
    pass
print("banner:", out.decode("utf-8", "replace")[:200])
s.sendall(WARRIOR.encode() + b"end\n")
time.sleep(2.0)
res = b""
try:
    while True:
        c = s.recv(8192)
        if not c:
            break
        res += c
except Exception:
    pass
txt = res.decode("utf-8", "replace")
print("=== RESULTAT ===")
print(txt[:1500])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else "non trouve")
s.close()
