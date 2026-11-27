p=r"./_z_55\_z_sc55_pwn.py"
s=open(p,encoding="utf-8").read()
# geometrie reelle : le 1er groom chunk est tasse depuis le top heap+0xc0 -> user heap+0xd0
s=s.replace("    p_addr = heap + 0x140","    p_addr = heap + 0xe0")
s=s.replace("heap + 0x140, 0x602050","heap + 0xe0, 0x602050")
# le chunk #76 a maintenant user 0x1890 et p+S+8 = 0x1898 = son data+8
s=s.replace("        elif made == 76:","        elif made == 76:")
open(p,"w",encoding="utf-8").write(s)
print("p>", [l for l in s.splitlines() if "0xe0" in l][:4])
