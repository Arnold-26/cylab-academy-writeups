import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\pachinko\server\programs\flag.bin"
d = open(p, "rb").read()
print("taille:", len(d))
print("hex:", d.hex())
print("repr:", repr(d))
print("ascii:", "".join(chr(c) if 32 <= c < 127 else "." for c in d))
# comparer avec nand_checker.bin
p2 = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\pachinko\server\programs\nand_checker.bin"
d2 = open(p2, "rb").read()
print("\nnand_checker.bin taille:", len(d2))
print("hex:", d2.hex()[:200])
