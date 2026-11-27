import sys, base64
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
data = bytes.fromhex("555055555c5e494f460353440a6c5307585f6b45094403466b5651550a0b0105514e")
print("len:", len(data))
transforms = {
    "xor_i": bytes(b ^ i for i, b in enumerate(data)),
    "sub_i": bytes((b - i) & 0xFF for i, b in enumerate(data)),
    "add_i": bytes((b + i) & 0xFF for i, b in enumerate(data)),
    "xor_prev": None,
}
prev = 0
out = bytearray()
for b in data:
    out.append(b ^ prev)
    prev = b
transforms["xor_prev"] = bytes(out)
for name, t in transforms.items():
    print(f"{name}: {t[:60]}")
    if b"academy{" in t or b"picoCTF{" in t or t.startswith(b"PK") or t.startswith(b"\x1f\x8b"):
        print("  >>> MATCH", name, t[:120])
