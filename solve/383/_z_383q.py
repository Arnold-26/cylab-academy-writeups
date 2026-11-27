import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\383_disk.img"
OFF = 731136 * 512
with open(p, "rb") as f:
    f.seek(OFF + 56274 * 4096)
    data = f.read(4096)
slack = data[12:].rstrip(b"\x00").decode("ascii", "replace")
phi = (1 + 5 ** 0.5) / 2
tokens = [t for t in slack.split(".") if t]


def variants(t):
    n = len(t)
    hi = sum(int(d) * phi ** (n - 1 - i) for i, d in enumerate(t) if d == "1")  # gauche = fort
    lo = sum(int(d) * phi ** i for i, d in enumerate(t) if d == "1")           # gauche = faible
    fr = sum(int(d) * phi ** (-(i + 1)) for i, d in enumerate(t) if d == "1")  # fraction
    return {"hi": hi, "lo": lo, "fr": fr}


best = []
for conv in ("hi", "lo", "fr"):
    for scale in (1, 16, 128, 255, 256):
        for rnd in ("round", "int", "ceil"):
            out = []
            for t in tokens:
                v = variants(t)[conv] * scale
                v = round(v) if rnd == "round" else (int(v) if rnd == "int" else int(v) + (v % 1 > 0))
                out.append(v)
            s = "".join(chr(x) if 32 <= x < 127 else "." for x in out)
            printable = sum(1 for c in s if c != ".")
            score = printable / len(s)
            best.append((score, conv, scale, rnd, s[:110]))
best.sort(reverse=True)
for b in best[:6]:
    print("score=%.2f conv=%s scale=%s rnd=%s\n   %s\n" % b)
