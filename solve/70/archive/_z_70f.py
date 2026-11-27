import sys, struct, zlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\70_investigative-reversing-0-mystery.png"
d = open(p, "rb").read()
print("taille:", len(d))
j = 8
while j + 8 <= len(d):
    ln = struct.unpack_from(">I", d, j)[0]
    typ = d[j + 4:j + 8]
    body = d[j + 8:j + 8 + ln]
    print("chunk %-6s len=%d" % (typ.decode("latin-1", "replace"), ln), end="")
    if typ in (b"tEXt", b"iTXt", b"zTXt", b"iCCP", b"pHYs", b"gAMA", b"bKGD"):
        print("  ->", repr(body[:200]))
    else:
        print()
    j += 12 + ln
    if typ == b"IEND":
        break
print("octets après IEND:", len(d) - j)
if len(d) > j:
    print("data:", d[j:j+200])
# recherche de motif lisible dans tout le fichier
for m in re.finditer(rb"[ -~]{12,}", d):
    s = m.group(0)
    if b"{" in s or b"flag" in s.lower() or b"academy" in s or b"pico" in s:
        print("  texte:", s[:120])
