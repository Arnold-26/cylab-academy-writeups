import sys, struct, zlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\o141\duck.png"
d = open(F, "rb").read()
j = 8
while j + 8 <= len(d):
    ln = struct.unpack_from(">I", d, j)[0]
    typ = d[j + 4:j + 8]
    body = d[j + 8:j + 8 + ln]
    if typ in (b"iTXt", b"tEXt", b"zTXt", b"iCCP"):
        print("=== %s (%d octets) ===" % (typ.decode(), ln))
        if typ == b"tEXt":
            print(body.replace(b"\x00", b" | ", 1).decode("latin-1", "replace"))
        elif typ == b"iTXt":
            print(repr(body)[:1200])
            try:
                print("\n--- texte ---")
                print(body.decode("utf-8", "replace")[:1200])
            except Exception:
                pass
        print()
    j += 12 + ln
    if typ == b"IEND":
        break
