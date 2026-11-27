import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pefile
P = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\win429\WinAntiDbg0x100.exe"
pe = pefile.PE(P)
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    dll = entry.dll.decode()
    if "kernel32" in dll.lower():
        print("DLL:", dll)
        for imp in entry.imports:
            print("   0x%-10x %s" % (imp.address, imp.name.decode() if imp.name else "?"))
# rechercher les motifs call [iat] pour les fonctions de debug
dbg_names = ("IsDebuggerPresent", "CheckRemoteDebuggerPresent", "NtQueryInformationProcess",
             "OutputDebugStringA", "OutputDebugStringW")
iat = {}
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in entry.imports:
        if imp.name and imp.name.decode() in dbg_names:
            iat[imp.name.decode()] = imp.address
print("\nIAT cibles:", {k: hex(v) for k, v in iat.items()})
d = open(P, "rb").read()
base = pe.OPTIONAL_HEADER.ImageBase
text = None
for s in pe.sections:
    if b".text" in s.Name:
        text = (s.VirtualAddress + base, s.PointerToRawData, s.Misc_VirtualSize)
        break
print("text:", [hex(x) for x in text])
va, off, size = text
for name, addr in iat.items():
    pat = b"\xff\x15" + addr.to_bytes(4, "little")
    idxs = []
    i = 0
    while True:
        i = d.find(pat, i)
        if i < 0:
            break
        idxs.append(i)
        i += 1
    print("%s : %d call [iat] a %s" % (name, len(idxs), [hex(x) for x in idxs[:5]]))
