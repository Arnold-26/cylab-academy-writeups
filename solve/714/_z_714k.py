import sys, base64, itertools, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
chunks = ['VVBVVVxeS', 'U9GA1NECm', 'xTB1hfa0U', 'JRANGa1ZR', 'VQoLAQVRT', 'g==']
best = []
for perm in itertools.permutations(chunks):
    s = "".join(perm)
    try:
        d = base64.b64decode(s + "=" * (-len(s) % 4))
    except Exception:
        continue
    m = FLAG.search(d)
    if m:
        print("FLAG direct:", m.group(0), "perm:", perm)
        best.append((100, d, perm))
        continue
    # single byte XOR
    for k in range(256):
        x = bytes(b ^ k for b in d)
        if b"academy{" in x or b"picoCTF{" in x:
            print("FLAG xor", k, ":", x, "perm:", perm)
            best.append((100, x, perm))
            break
    # score imprimable
    for k in range(256):
        x = bytes(b ^ k for b in d)
        printable = sum(1 for b in x if 32 <= b < 127)
        if printable >= len(x) - 2:
            best.append((printable, x, perm))
print("candidats imprimables:", len(best))
for sc, x, perm in sorted(best, key=lambda t: -t[0])[:5]:
    print(sc, perm, x[:60])
