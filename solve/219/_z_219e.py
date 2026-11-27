import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/219_riscy"
d = open(p, "rb").read()
ct = d[0x210:0x210 + 52]
print("chiffre:", ct.hex())


def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    out = bytearray()
    i = j = 0
    for b in data:
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        out.append(b ^ S[(S[i] + S[j]) & 0xFF])
    return bytes(out)


for key in (b"picoCTF{", b"academy{"):
    pt = rc4(key, ct)
    print(f"cle={key}: {pt}")
