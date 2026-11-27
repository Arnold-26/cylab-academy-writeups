import sys, zlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_iw/b3.bin"
d = open(p, "rb").read()
print("taille:", len(d), "debut:", d[:8].hex())
for i in range(min(128, len(d))):
    try:
        o = zlib.decompress(d[i:])
        print("offset", i, "-> decompresse", len(o))
        print(o[:400])
        break
    except Exception:
        pass
else:
    print("pas de zlib valide")
