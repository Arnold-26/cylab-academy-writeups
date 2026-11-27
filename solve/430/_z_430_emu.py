import struct, sys
from unicorn import *
from unicorn.x86_const import *

def parse_sections(path):
    b = open(path, 'rb').read()
    e_lfanew = struct.unpack_from('<I', b, 0x3C)[0]
    assert b[e_lfanew:e_lfanew+4] == b'PE\0\0'
    coff = e_lfanew + 4
    nsec = struct.unpack_from('<H', b, coff + 2)[0]
    opt = coff + 20
    magic = struct.unpack_from('<H', b, opt)[0]
    pe32plus = magic == 0x20b
    image_base = struct.unpack_from('<Q' if pe32plus else '<I', b, opt + 24 if pe32plus else opt + 28)[0]
    size_of_image = struct.unpack_from('<I', b, opt + 56)[0]
    sec_tab = opt + struct.unpack_from('<H', b, coff + 16)[0]
    secs = []
    for i in range(nsec):
        o = sec_tab + i * 40
        name = b[o:o+8].rstrip(b'\0').decode('latin1')
        vsize, vaddr, rawsize, rawptr = struct.unpack_from('<IIII', b, o + 8)
        secs.append((name, vaddr, vsize, rawptr, rawsize))
    return b, image_base, size_of_image, secs

def load(path):
    b, base, soimage, secs = parse_sections(path)
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    IMG = base
    uc.mem_map(IMG, (soimage + 0xFFF) & ~0xFFF, UC_PROT_ALL)
    for name, vaddr, vsize, rawptr, rawsize in secs:
        if rawsize:
            uc.mem_write(IMG + vaddr, b[rawptr:rawptr+rawsize])
    return uc, b, base, soimage, secs

def run_func(uc, addr, args, ret=0x999000, stack=0x200000, stacksz=0x10000):
    try:
        uc.mem_map(stack, stacksz)
    except UcError:
        pass
    try:
        uc.mem_map(ret & ~0xFFF, 0x1000)
    except UcError:
        pass
    sp = stack + stacksz - 0x100
    for a in reversed(args):
        sp -= 4
        uc.mem_write(sp, struct.pack('<I', a & 0xFFFFFFFF))
    sp -= 4
    uc.mem_write(sp, struct.pack('<I', ret))
    uc.reg_write(UC_X86_REG_ESP, sp)
    uc.reg_write(UC_X86_REG_EBP, 0)
    uc.emu_start(addr, ret, count=20_000_000)
    return uc.reg_read(UC_X86_REG_EAX)

if __name__ == '__main__':
    exe = sys.argv[1]
    cfg = sys.argv[2]
    MUT = int(sys.argv[3], 16)
    DEC = int(sys.argv[4], 16)
    G_SIZE = int(sys.argv[5], 16)
    G_BUF = int(sys.argv[6], 16)
    G_FLAG = int(sys.argv[7], 16)

    raw = open(cfg, 'rb').read()
    size = struct.unpack('<I', raw[:4])[0]
    data = raw[4:]
    print(f"config: size={size} datalen={len(data)}")

    uc, b, base, soimage, secs = load(exe)
    BUFVA = 0x00100000
    uc.mem_map(BUFVA, 0x1000)
    uc.mem_write(BUFVA, data + b'\0' * (0x1000 - len(data)))
    # globals
    uc.mem_write(G_SIZE, struct.pack('<I', size))
    uc.mem_write(G_BUF, struct.pack('<I', BUFVA))
    uc.mem_write(G_FLAG, struct.pack('<I', BUFVA + size + 1))

    before = bytes(uc.mem_read(BUFVA, size))
    run_func(uc, MUT, [1])
    after = bytes(uc.mem_read(BUFVA, size))
    print("letters avant :", before)
    print("cle muee      :", after)

    run_func(uc, DEC, [BUFVA])
    flag = bytes(uc.mem_read(BUFVA + size + 1, size))
    print("FLAG          :", flag)
    print("               ", flag.decode('utf-8', 'replace'))
