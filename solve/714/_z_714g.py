import sys, base64, itertools, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
chunks = ['VVBVVVxeS', 'U9GA1NECm', 'xTB1hfa0U', 'JRANGa1ZR', 'VQoLAQVRT', 'g==']
headers = [b"PK", b"\x1f\x8b", b"\x89PNG", b"%PDF", b"RIFF", b"academy{", b"picoCTF{"]
best = []
for perm in itertools.permutations(chunks):
    s = "".join(perm)
    try:
        d = base64.b64decode(s + "=" * (-len(s) % 4))
    except Exception:
        continue
    for h in headers:
        if d.startswith(h):
            print("HEADER", h, "perm:", perm, d[:40])
    m = FLAG.search(d)
    if m:
        print("FLAG:", m.group(0), "perm:", perm)
        best.append((perm, m.group(0)))
print("permutations avec flag:", len(best))
