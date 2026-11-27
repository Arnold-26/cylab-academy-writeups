p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
s=s.replace("        vals = pay[2:] + [0, 0]\n        for i in range(11):\n            creams[i] = vals[i]",
            "        vals = pay[2:] + [0, 0]\n        # le read de 0x58 o couvre 0x602130..0x602188 = creams[0..8] seulement\n        for i in range(9):\n            creams[i] = vals[i]")
s=s.replace("s = [i for i in range(11) if creams[i] == 0][0]","s = [i for i in range(9) if creams[i] == 0][0]")
s=s.replace("free_low = [i for i in range(11) if creams[i] == 0]","free_low = [i for i in range(9) if creams[i] == 0]")
open(p,"w",encoding="utf-8").write(s)
print("patched", s.count("range(9)"))
