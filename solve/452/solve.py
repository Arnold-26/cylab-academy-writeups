# 452 - Binary Instrumentation 2  (Reverse Engineering, picoCTF 2025)
# Flag: academy{fr1da_f0r_b1n_in5trum3nt4tion!_b21aef39}
# Write-up: ../../../writeups/reverse-engineering/452-binary-instrumentation-2.md
# This is the script that produced the flag; historical variants are in archive/.
#
import struct, math, collections, sys

def sections(path):
    b = open(path, 'rb').read()
    e = struct.unpack_from('<I', b, 0x3C)[0]
    assert b[e:e+4] == b'PE\0\0'
    coff = e + 4
    nsec = struct.unpack_from('<H', b, coff + 2)[0]
    optsize = struct.unpack_from('<H', b, coff + 16)[0]
    opt = coff + 20
    magic = struct.unpack_from('<H', b, opt)[0]
    plus = magic == 0x20b
    ep = struct.unpack_from('<I', b, opt + 16)[0]
    ib = struct.unpack_from('<Q' if plus else '<I', b, opt + 24 if plus else opt + 28)[0]
    sec = opt + optsize
    out = []
    for i in range(nsec):
        o = sec + i * 40
        name = b[o:o+8].rstrip(b'\0').decode('latin1')
        vsize, va, rawsize, rawptr = struct.unpack_from('<IIII', b, o + 8)
        out.append((name, va, vsize, rawptr, rawsize))
    return b, ib, ep, out


def ent(d):
    if not d:
        return 0
    c = collections.Counter(d)
    n = len(d)
    return -sum(v / n * math.log2(v / n) for v in c.values())


for path in sys.argv[1:]:
    b, ib, ep, secs = sections(path)
    print("=====", path, "imagebase", hex(ib), "entry", hex(ib + ep))
    for name, va, vsize, rawptr, rawsize in secs:
        d = b[rawptr:rawptr + rawsize] if rawsize else b''
        zero = d.count(0) / max(1, len(d))
        print("  %-8s va=%#x vsize=%#x raw=%#x  entropy=%.2f  zeros=%.1f%%" %
              (name, va, vsize, rawsize, ent(d), 100 * zero))
    for name, va, vsize, rawptr, rawsize in secs:
        if name in ('.ATOM', '.data', '.rdata'):
            d = b[rawptr:rawptr + 96]
            print("  %s[:96] = %s" % (name, d.hex()))
