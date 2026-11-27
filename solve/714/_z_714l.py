import sys, base64, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
raw = "VVBVVVxeSU9GA1NECmxTB1hfa0UJRANGa1ZRVQoLAQVRTg=="
data = base64.b64decode(raw)
print("data:", data.hex())
imsis = ["310410743419304", "310410", "94309", "23104", "00101"]
for imsi in imsis:
    keys = [imsi.encode(), bytes(int(c) for c in imsi), bytes(int(c) + 48 for c in imsi)]
    for k in keys:
        if not k:
            continue
        x = bytes(b ^ k[i % len(k)] for i, b in enumerate(data))
        ok = sum(1 for b in x if 32 <= b < 127) / len(x)
        if ok > 0.9 or FLAG.search(x):
            print(f"imsi={imsi} key={k[:20]} -> {x[:60]} ({ok:.2f})")
# essai : la donnee est-elle du base64 d'un XOR avec un byte unique qui donne 'academy{' ?
# on teste si data XOR key donne un texte base64 valide
print("\n=== data comme base64 d'une autre base64 ? ===")
for k in range(256):
    x = bytes(b ^ k for b in data)
    try:
        y = base64.b64decode(x)
        if FLAG.search(y):
            print("double b64 xor", k, y)
    except Exception:
        pass
