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
s = socket.create_connection((HOST, PORT), timeout=90)
s.settimeout(90)
time.sleep(0.5)
try:
    print("banner:", s.recv(8192).decode("utf-8", "replace")[:300])
except Exception as e:
    print("(pas de banner)", type(e).__name__)
s.sendall(RULE.encode())
try:
    s.shutdown(socket.SHUT_WR)
except Exception:
    pass
out = b""
t0 = time.time()
while time.time() - t0 < 90:
    try:
        c = s.recv(16384)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("utf-8", "replace")
print("=== reponse ===")
print(txt[:1500])
import re
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else None)
