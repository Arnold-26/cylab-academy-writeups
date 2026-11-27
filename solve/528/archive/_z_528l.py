import sys, base64, binascii
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s = "MFRWCZDFNV4XWMLUL53TI43OG5PWQNDSMRPXK3TSGR3DG3BRNY4V65DIGNPW2MDCGFWDGX3DGBSDG7I="
print("len:", len(s))
for name, fn in (("base32", base64.b32decode), ("base32hex", base64.b32hexdecode)):
    try:
        d = fn(s + "=" * ((8 - len(s) % 8) % 8))
        print(name, "->", d)
    except Exception as e:
        print(name, "ERR", type(e).__name__, e)
try:
    print("b64 ->", base64.b64decode(s + "=" * ((4 - len(s) % 4) % 4)))
except Exception as e:
    print("b64 ERR", type(e).__name__)
