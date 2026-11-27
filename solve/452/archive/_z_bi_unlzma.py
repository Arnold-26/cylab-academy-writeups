import struct, lzma, sys, os

def sections(path):
    b = open(path, 'rb').read()
    e = struct.unpack_from('<I', b, 0x3C)[0]
    coff = e + 4
    nsec = struct.unpack_from('<H', b, coff + 2)[0]
    optsize = struct.unpack_from('<H', b, coff + 16)[0]
    opt = coff + 20
    ib = struct.unpack_from('<Q', b, opt + 24)[0]
    sec = opt + optsize
    out = {}
    for i in range(nsec):
        o = sec + i * 40
        name = b[o:o+8].rstrip(b'\0').decode('latin1')
        vsize, va, rawsize, rawptr = struct.unpack_from('<IIII', b, o + 8)
        out[name] = (b[rawptr:rawptr+rawsize], ib + va, vsize)
    return out

for path in sys.argv[1:]:
    s = sections(path)
    blob, va, vsize = s['.ATOM']
    print("=====", path, "ATOM", len(blob), "octets")
    props = blob[0]
    lc = props % 9
    rem = props // 9
    lp = rem % 5
    pb = rem // 5
    dsize = struct.unpack_from('<I', blob, 1)[0]
    usize = struct.unpack_from('<Q', blob, 5)[0]
    print("  lzma props: lc=%d lp=%d pb=%d dict=%d  uncompressed_size=%d (0x%x)" % (lc, lp, pb, dsize, usize, usize))
    d = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
    try:
        out = d.decompress(blob)
    except Exception as ex:
        print("  ERREUR:", ex)
        continue
    print("  decompresse:", len(out), "octets ; eof=", d.eof)
    outpath = "/tmp/bi/" + os.path.basename(path).replace('.exe', '') + "_payload.bin"
    open(outpath, 'wb').write(out)
    print("  ecrit:", outpath)
    print("  debut:", out[:64].hex())
    if out[:2] == b'MZ':
        print("  *** c'est un PE ***")
