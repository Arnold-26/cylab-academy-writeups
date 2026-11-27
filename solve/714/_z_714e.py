import sys, base64, itertools, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
chunks = ["VVBVVVxeS", "U9GA1NECm", "xTB1hfa0U", "JRANGa1ZR", "VQoLAQVT", "g=="]
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
found = False
for perm in itertools.permutations(chunks):
    s = "".join(perm)
    try:
        d = base64.b64decode(s + "=" * (-len(s) % 4))
    except Exception:
        continue
    if FLAG.search(d):
        print("FLAG (perm):", FLAG.search(d).group(0))
        found = True
        break
    if d.startswith(b"PK") or d.startswith(b"\x1f\x8b") or d.startswith(b"\x89PNG"):
        print("HEADER (perm):", d[:8].hex(), "ordre:", perm)
print("permutations testees, flag trouve:", found)
# essai XOR avec cles plausibles sur le decodage standard
data = base64.b64decode("VVBVVVxeSU9GA1NECmxTB1hfa0UJRANGa1ZRVQoLAQVTg==")
keys = [b"94309", b"310410743419304", b"310410", b"23104", b"network", b"carrier"]
for k in keys:
    x = bytes(b ^ k[i % len(k)] for i, b in enumerate(data))
    print(k, "->", x[:50])
    if FLAG.search(x):
        print("FLAG (xor):", FLAG.search(x).group(0))
