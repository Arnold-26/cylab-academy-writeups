import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\182_wasm.bin"
d = open(p, "rb").read()
print("taille:", len(d))
# le flag attendu est souvent construit char par char (XOR/add) ; chercher les gros blocs de donnees
# on affiche les 600 derniers octets en hex+ascii
tail = d[-800:]
for i in range(0, len(tail), 32):
    chunk = tail[i:i+32]
    hexs = " ".join("%02x" % c for c in chunk)
    asc = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
    print("%04x  %-95s %s" % (len(d) - 800 + i, hexs, asc))
