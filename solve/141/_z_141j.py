import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s1 = "YO[\\N\\ME(IS_tNE)50uP?^DId_YOu(]E@t*mY_3RD()B2g3l?"
s2 = "8,:8+14>Fx0l+$*KjVD>[o*.;+1|*[n&2G^201l&,Mv+_'T_B"
b1 = s1.encode("utf-8")
b2 = s2.encode("utf-8")
print("len1:", len(b1), "len2:", len(b2))
out = bytes(b2[i] ^ b1[i] for i in range(len(b2)))
print("brut:", out)
try:
    txt = out.decode("utf-8")
    print("texte:", txt)
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    print("FLAG:", m.group(0) if m else None)
except Exception as e:
    print("decode err", e)
