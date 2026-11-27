p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
s=s.replace("            ptr = o[0x120:0x126]","            log.warning('LEAKGEO tail=%s' % o[0x100:0x150].hex())\n            ptr = o[0x100:0x150][0x20:0x26]")
open(p,"w",encoding="utf-8").write(s)
