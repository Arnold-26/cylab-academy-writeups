import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pefile
P = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\wine317\vuln.exe"
pe = pefile.PE(P)
print("protege ASLR:", bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x40))
# symboles
try:
    for sym in pe.DIRECTORY_ENTRY_IMPORT:
        pass
except Exception:
    pass
syms = []
if hasattr(pe, "DIRECTORY_ENTRY_EXPORT") and pe.DIRECTORY_ENTRY_EXPORT:
    for s in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        syms.append((s.address, s.name))
print("exports:", syms[:10])
# recherche de la chaine flag.txt et des references
d = open(P, "rb").read()
i = d.find(b"flag.txt")
print("flag.txt a l'offset fichier:", i, "-> RVA ~", hex(i - 0x400 + 0x9000) if i > 0 else None)
# chercher dans .rdata
for s in pe.sections:
    nm = s.Name.decode(errors="replace").strip("\x00")
    if b"flag.txt" in s.get_data():
        off = s.get_data().find(b"flag.txt")
        print("section %s contient flag.txt a RVA %s" % (nm, hex(s.VirtualAddress + off)))
# desassembler vuln et win a partir des chaines
print("\n=== recherche des fonctions via pdata/symboles COFF ===")
print("nb symboles:", pe.FILE_HEADER.NumberOfSymbols, "| pointeur:", pe.FILE_HEADER.PointerToSymbolTable)
