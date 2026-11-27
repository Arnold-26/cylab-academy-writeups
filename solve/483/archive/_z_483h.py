import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 47902
RULE = r'''rule CyLab_FakeMalware
{
    strings:
        $mz = {4D 5A}
        $name1 = "YaraRules0x100"
        $upx = "UPX"
        $ntq = "NtQuery"
        $dbg = "debugger process" wide ascii
        $fake = "fake malware" wide ascii nocase
    condition:
        ($mz and ($name1 or $fake)) or $dbg
}
'''
print("=== test 1 : attendre sans rien envoyer ===")
s = socket.create_connection((HOST, PORT), timeout=30)
s.settimeout(5)
time.sleep(3)
try:
    b = s.recv(8192)
    print("recu sans envoi:", b.decode("utf-8", "replace")[:300])
except socket.timeout:
    print("(aucun banner en 3s)")
s.close()

print("\n=== test 2 : envoyer puis attendre sans shutdown ===")
s = socket.create_connection((HOST, PORT), timeout=60)
s.settimeout(60)
s.sendall(RULE.encode())
time.sleep(1)
out = b""
t0 = time.time()
while time.time() - t0 < 60:
    try:
        c = s.recv(16384)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("utf-8", "replace")
print(txt[:1200])
import re
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
