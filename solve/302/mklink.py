#!/usr/bin/env python3
"""Minimal eBPF (EM_BPF) shared-object linker.

Solana's rbpf loader requires an ET_DYN / EM_BPF ELF whose .text/.rodata
addresses equal their file offsets, plus DT_REL/DT_SYMTAB/DT_STRTAB dynamic
entries so it can resolve syscall calls by symbol name.

Takes the clang-produced relocatable object and emits such an ELF:
  * calls (R_BPF_64_32)  -> dynamic reloc, imm set to -1 (loader patches the hash)
  * lddw  (R_BPF_64_64)  -> statically resolved, plus an R_X86_64_RELATIVE-style
                            reloc so the loader rebases it to MM_PROGRAM_START
"""
import struct
import sys

EM_BPF = 247
ET_DYN = 3
SHT_NULL, SHT_PROGBITS, SHT_SYMTAB, SHT_STRTAB, SHT_REL, SHT_DYNAMIC, SHT_DYNSYM = 0, 1, 2, 3, 9, 6, 11
SHF_WRITE, SHF_ALLOC, SHF_EXECINSTR = 1, 2, 4
PT_LOAD, PT_DYNAMIC = 1, 2

R_BPF_64_64 = 1
R_BPF_64_32 = 10
R_BPF_64_RELATIVE = 8  # x86_64 RELATIVE, what rbpf maps to Bpf_64_Relative


def align(x, a):
    return (x + a - 1) // a * a


def cstr(tab, off):
    e = tab.find(b"\0", off)
    return tab[off:e].decode("latin1")


class Sec:
    pass


def parse(path):
    d = open(path, "rb").read()
    assert d[:4] == b"\x7fELF", "not an ELF"
    fields = struct.unpack_from("<HHIQQQIHHHHHH", d, 16)
    (e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags,
     e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx) = fields
    secs = []
    for i in range(e_shnum):
        off = e_shoff + i * e_shentsize
        (sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size,
         sh_link, sh_info, sh_addralign, sh_entsize) = struct.unpack_from("<IIQQQQIIQQ", d, off)
        s = Sec()
        s.type, s.flags, s.addr, s.offset, s.size = sh_type, sh_flags, sh_addr, sh_offset, sh_size
        s.link, s.info, s.align, s.entsize, s.name_off = sh_link, sh_info, sh_addralign, sh_entsize, sh_name
        s.data = d[sh_offset:sh_offset + sh_size]
        secs.append(s)
    shstr = secs[e_shstrndx].data
    for s in secs:
        s.name = cstr(shstr, s.name_off)
    return d, secs, e_machine, e_type


def read_syms(sec, strtab):
    out = []
    for off in range(0, len(sec.data), 24):
        st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from(
            "<IBBHQQ", sec.data, off)
        out.append(dict(name=cstr(strtab, st_name) if st_name else "",
                        info=st_info, other=st_other, shndx=st_shndx,
                        value=st_value, size=st_size))
    return out


def main(obj_path, so_path, entryname="entrypoint"):
    d, secs, e_machine, e_type = parse(obj_path)
    assert e_machine == EM_BPF, f"input is not EM_BPF (got {e_machine})"
    byname = {s.name: s for s in secs}

    text_s = byname[".text"]
    symtab_s = byname[".symtab"]
    strtab = byname[strtab_s.link].data if False else secs[symtab_s.link].data
    syms = read_syms(symtab_s, strtab)

    # ---- collect allocatable read-only data sections (rbpf concatenates these)
    RO_NAMES = (".rodata", ".data.rel.ro", ".eh_frame")
    ro_secs = [s for s in secs if s.name in RO_NAMES or s.name.startswith(".rodata")]
    text = bytearray(text_s.data)

    # ---- output layout
    PHNUM = 3
    hdr_end = 64 + PHNUM * 56
    text_off = align(hdr_end, 16)
    text_end = text_off + len(text)

    ro_off = align(text_end, 8)
    ro_blob = bytearray()
    sec_out = {}
    for s in ro_secs:
        while len(ro_blob) % max(s.align, 1) != 0:
            ro_blob.append(0)
        sec_out[id(s)] = ro_off + len(ro_blob)
        ro_blob += s.data
    ro_len = len(ro_blob)

    # ---- relocation processing
    dyn_needed = []       # ordered list of undefined symbol names
    dyncalls = []         # (out_insn_off, name)
    rel8 = []             # (out_insn_off,) instructions needing MM rebase
    for rs in [s for s in secs if s.type == SHT_REL]:
        for off in range(0, len(rs.data), 16):
            r_offset, r_info = struct.unpack_from("<QQ", rs.data, off)
            r_sym = r_info >> 32
            r_type = r_info & 0xFFFFFFFF
            sym = syms[r_sym]
            if r_type == R_BPF_64_32:
                insn = r_offset
                # imm = -1 marks "resolve me by symbol name"
                struct.pack_into("<i", text, insn + 4, -1)
                if sym["shndx"] == 0:  # undefined -> syscall
                    name = sym["name"]
                    if name not in dyn_needed:
                        dyn_needed.append(name)
                    dyncalls.append((text_off + insn, name))
                else:
                    raise SystemExit(f"internal call reloc unsupported: {sym['name']}")
            elif r_type == R_BPF_64_64:
                addend = struct.unpack_from("<q", text, r_offset + 4)[0]
                if sym["shndx"] != 0:
                    tgt_sec = secs[sym["shndx"]]
                    base = sec_out[id(tgt_sec)]
                    value = base + sym["value"] + addend
                else:
                    raise SystemExit(f"undefined lddw symbol: {sym['name']}")
                struct.pack_into("<Q", text, r_offset + 4, value)
                rel8.append(text_off + r_offset)
            else:
                raise SystemExit(f"unsupported relocation type {r_type}")

    # ---- entrypoint
    ep = [s for s in syms if s["name"] == entryname]
    assert len(ep) == 1, f"{entryname} symbol not found/unique"
    e_entry = text_off + ep[0]["value"]

    # ---- .dynsym / .dynstr
    dynstr = bytearray(b"\0")
    name_off = {}

    def intern(n):
        if n not in name_off:
            name_off[n] = len(dynstr)
            dynstr.extend(n.encode() + b"\0")
        return name_off[n]

    dynsym = [struct.pack("<IBBHQQ", 0, 0, 0, 0, 0, 0)]  # null symbol
    for n in dyn_needed:
        dynsym.append(struct.pack("<IBBHQQ", intern(n), 0x10, 0, 0, 0, 0))  # GLOBAL NOTYPE UNDEF
    ep_dyn_idx = len(dynsym)
    dynsym.append(struct.pack("<IBBHQQ", intern(entryname), 0x12, 0, 1, e_entry, len(text)))
    syment = 24

    # ---- .rel.dyn
    rels = []
    for insn_off, name in dyncalls:
        idx = 1 + dyn_needed.index(name)
        rels.append(struct.pack("<QQ", insn_off, (idx << 32) | R_BPF_64_32))
    for insn_off in rel8:
        rels.append(struct.pack("<QQ", insn_off, (0 << 32) | R_BPF_64_RELATIVE))

    # ---- lay out the file
    dynsym_off = align(ro_off + ro_len, 8)
    dynstr_off = dynsym_off + syment * len(dynsym)
    reldyn_off = align(dynstr_off + len(dynstr), 8)
    dynamic_off = align(reldyn_off + 16 * len(rels), 8)
    dynamic = [
        (0x11, reldyn_off),              # DT_REL
        (0x12, 16 * len(rels)),          # DT_RELSZ
        (0x13, 16),                      # DT_RELENT
        (0x06, dynsym_off),              # DT_SYMTAB
        (0x0B, syment),                  # DT_SYMENT
        (0x05, dynstr_off),              # DT_STRTAB
        (0x0A, len(dynstr)),             # DT_STRSZ
        (0x00, 0),                       # DT_NULL
    ]
    dyn_blob = b"".join(struct.pack("<qQ", t, v) for t, v in dynamic)

    # .symtab + .strtab (nice-to-have symbol names; rbpf checks funcs are inside .text)
    strtab2 = bytearray(b"\0")
    symtab_blob = struct.pack("<IBBHQQ", 0, 0, 0, 0, 0, 0)
    e_off = len(strtab2)
    strtab2.extend(entryname.encode() + b"\0")
    symtab_blob += struct.pack("<IBBHQQ", e_off, 0x12, 0, 1, e_entry, len(text))
    symtab_off = align(dynamic_off + len(dyn_blob), 8)
    strtab2_off = symtab_off + len(symtab_blob)

    shstr = bytearray(b"\0")
    shname = {}

    def shintern(n):
        if n not in shname:
            shname[n] = len(shstr)
            shstr.extend(n.encode() + b"\0")
        return shname[n]

    names = ["", ".text", ".rodata", ".dynsym", ".dynstr", ".rel.dyn", ".dynamic",
             ".symtab", ".strtab", ".shstrtab"]
    for n in names:
        shintern(n)
    shstr_off = strtab2_off + len(strtab2)
    sh_table_off = align(shstr_off + len(shstr), 8)
    nsh = len(names)
    file_size = sh_table_off + 64 * nsh

    out = bytearray(file_size)
    # ELF header
    e_ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + bytes(8)
    struct.pack_into("<16sHHIQQQIHHHHHH", out, 0, e_ident, ET_DYN, EM_BPF, 1, e_entry,
                     64, sh_table_off, 0, 64, 56, PHNUM, 64, nsh, 9)
    # program headers
    struct.pack_into("<IIQQQQQQ", out, 64,
                     PT_LOAD, 5, 0, 0, 0, text_end, text_end, 0x1000)
    struct.pack_into("<IIQQQQQQ", out, 64 + 56,
                     PT_LOAD, 4, ro_off, ro_off, ro_off, dynamic_off + len(dyn_blob) - ro_off,
                     dynamic_off + len(dyn_blob) - ro_off, 0x1000)
    struct.pack_into("<IIQQQQQQ", out, 64 + 112,
                     PT_DYNAMIC, 6, dynamic_off, dynamic_off, dynamic_off, len(dyn_blob), len(dyn_blob), 8)

    out[text_off:text_off + len(text)] = text
    out[ro_off:ro_off + ro_len] = ro_blob
    out[dynsym_off:dynsym_off + syment * len(dynsym)] = b"".join(dynsym)
    out[dynstr_off:dynstr_off + len(dynstr)] = dynstr
    out[reldyn_off:reldyn_off + 16 * len(rels)] = b"".join(rels)
    out[dynamic_off:dynamic_off + len(dyn_blob)] = dyn_blob
    out[symtab_off:symtab_off + len(symtab_blob)] = symtab_blob
    out[strtab2_off:strtab2_off + len(strtab2)] = strtab2
    out[shstr_off:shstr_off + len(shstr)] = shstr

    shdrs = [
        (0, SHT_NULL, 0, 0, 0, 0, 0, 0, 0, 0),
        (shname[".text"], SHT_PROGBITS, SHF_ALLOC | SHF_EXECINSTR, text_off, text_off, len(text), 0, 0, 8, 0),
        (shname[".rodata"], SHT_PROGBITS, SHF_ALLOC, ro_off, ro_off, ro_len, 0, 0, 1, 0),
        (shname[".dynsym"], SHT_DYNSYM, SHF_ALLOC, dynsym_off, dynsym_off, syment * len(dynsym), 4, 1, 8, syment),
        (shname[".dynstr"], SHT_STRTAB, SHF_ALLOC, dynstr_off, dynstr_off, len(dynstr), 0, 0, 1, 0),
        (shname[".rel.dyn"], SHT_REL, SHF_ALLOC, reldyn_off, reldyn_off, 16 * len(rels), 3, 0, 8, 16),
        (shname[".dynamic"], SHT_DYNAMIC, SHF_ALLOC | SHF_WRITE, dynamic_off, dynamic_off,
         len(dyn_blob), 4, 0, 8, 16),
        (shname[".symtab"], SHT_SYMTAB, 0, symtab_off, symtab_off, len(symtab_blob), 8, 1, 8, 24),
        (shname[".strtab"], SHT_STRTAB, 0, strtab2_off, strtab2_off, len(strtab2), 0, 0, 1, 0),
        (shname[".shstrtab"], SHT_STRTAB, 0, shstr_off, shstr_off, len(shstr), 0, 0, 1, 0),
    ]
    for i, (nm, ty, fl, addr, off, size, link, info, al, ent) in enumerate(shdrs):
        struct.pack_into("<IIQQQQIIQQ", out, sh_table_off + 64 * i,
                         nm, ty, fl, addr, off, size, link, info, al, ent)

    open(so_path, "wb").write(out)
    print(f"[+] wrote {so_path}: {len(out)} bytes")
    print(f"    .text  off/addr=0x{text_off:x} size={len(text)}")
    print(f"    .rodata off/addr=0x{ro_off:x} size={ro_len}")
    print(f"    entrypoint vaddr=0x{e_entry:x}")
    print(f"    dynsyms={len(dynsym)} (entrypoint idx {ep_dyn_idx}) syscalls={dyn_needed}")
    print(f"    rel.dyn={len(rels)} (calls={len(dyncalls)}, rebase={len(rel8)})")
    print(f"    symtab off=0x{symtab_off:x} extent=0x{file_size:x}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
