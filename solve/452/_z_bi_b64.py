import base64, re, sys

for path in sys.argv[1:]:
    b = open(path, 'rb').read()
    print("=====", path)
    hits = set()
    for m in re.finditer(rb'[A-Za-z0-9+/]{16,}={0,2}', b):
        s = m.group(0)
        if len(s) % 4:
            s = s[:len(s) // 4 * 4]
        try:
            dec = base64.b64decode(s, validate=True)
        except Exception:
            continue
        if b'academy{' in dec or b'picoCTF{' in dec:
            hits.add(dec[dec.find(b'academy{') if b'academy{' in dec else dec.find(b'picoCTF{'):][:80])
    for h in sorted(hits):
        print("  BASE64 ->", h)
    # recherche directe de chaines academy dans le binaire et en rot13
    for pat in (rb'academy\{[^}]{0,80}\}', rb'picoCTF\{[^}]{0,80}\}'):
        for m in re.finditer(pat, b):
            print("  DIRECT ->", m.group(0))
