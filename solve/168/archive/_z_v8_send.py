#!/usr/bin/env python3
"""Send a JS exploit to a CyLab/picoCTF d8 service.
usage: _z_v8_send.py host port file.js [timeout]
"""
import sys, re
from pwn import remote, context

context.log_level = 'error'

host, port, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 30
script = open(path, 'rb').read()

io = remote(host, port, timeout=timeout)
io.recvuntil(b'5k:', timeout=timeout)
io.sendline(str(len(script)).encode())
io.recvuntil(b'please!!', timeout=timeout)
io.send(script)
data = io.recvall(timeout=timeout)
io.close()
sys.stdout.write(data.decode('utf-8', 'replace'))
print("\n===== END =====")
