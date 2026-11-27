import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
try:
    import pefile
except ImportError:
    print("pefile absent")
    pefile = None
P = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\win429\WinAntiDbg0x100.exe"
if pefile:
    pe = pefile.PE(P)
    print("machine:", hex(pe.FILE_HEADER.Machine), "| imagebase:", hex(pe.OPTIONAL_HEADER.ImageBase))
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        print("DLL:", entry.dll.decode())
        for imp in entry.imports:
            print("   0x%-8x %s" % (imp.address, imp.name.decode() if imp.name else "?"))
else:
    d = open(P, "rb").read()
    print("taille:", len(d))
    for n in (b"IsDebuggerPresent", b"CheckRemoteDebuggerPresent", b"NtQueryInformationProcess",
              b"OutputDebugStringA", b"OutputDebugStringW", b"GetTickCount"):
        print(n, "->", d.find(n))
