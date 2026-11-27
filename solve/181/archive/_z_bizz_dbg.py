import re, sys
exec(open('/tmp/_z_bizz_gen.py').read().split("HOP = ")[0])
print("fn_end(0x813d5dc) =", hex(fn_end(0x813d5dc)))
ev = events(0x813d5dc, fn_end(0x813d5dc))
print("nb events:", len(ev))
for e in ev[:40]:
    print("  ", hex(e[0]), e[1], hex(e[2]) if isinstance(e[2], int) else e[2])
