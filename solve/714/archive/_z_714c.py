import sys, base64, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
chunks = ["565642565656786553", "55394741314e45436d", "785442316866613055",
          "4a52414e4761315a52", "56516f4c4151565254", "673d3d"]
raw = "".join(bytes.fromhex(c).decode("latin-1") for c in chunks)
print("brut concatene:", raw)
try:
    d1 = base64.b64decode(raw + "=" * (-len(raw) % 4))
    print("decode1:", d1, d1.hex())
    try:
        d2 = base64.b64decode(d1)
        print("decode2:", d2)
    except Exception as e:
        print("pas de double base64:", e)
    # essai XOR simple
    for k in range(256):
        x = bytes(b ^ k for b in d1)
        if b"academy{" in x or b"picoCTF{" in x:
            print("XOR", k, x)
except Exception as e:
    print("err:", e)
