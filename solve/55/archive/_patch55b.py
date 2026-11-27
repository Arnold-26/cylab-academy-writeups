p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
old="    creams[0] = FAKE_FAST\n    creams[1] = 0x602050\n"
new=("    creams[0] = FAKE_FAST\n    creams[1] = 0x602050\n"
     "    # les 4 buy(0x58) de la stage 1b ont rempli les slots 2..5 (pointeurs tas reels)\n"
     "    creams[2] = creams[3] = creams[4] = creams[5] = 1\n")
assert old in s
s=s.replace(old,new)
open(p,"w",encoding="utf-8").write(s)
print("ok")
