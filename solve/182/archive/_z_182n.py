import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
stored = bytes.fromhex("7b7f780f0675153e0f1b694e0c0f78393d0a117e4d3d5810641050082a3a3b01102f16690710321f")
for pfx in ("academy{", "picoCTF{"):
    print("=== prefixe suppose: %s ===" % pfx)
    for i, ch in enumerate(pfx):
        key = stored[i] ^ ord(ch)
        print("  i=%2d stored=%02x char=%02x key=%02x" % (i, stored[i], ord(ch), key))
    print()
# pattern attendu: key = 20 ^ parite ^ mod3 ( ^ i%10 ? )
for i in range(8):
    base = 20 ^ (9 if i % 2 == 0 else 8) ^ (7 if i % 3 == 0 else (6 if i % 3 == 1 else 5))
    base10 = base ^ (i % 10)
    print("i=%d : 20^parite^mod3 = %02x | avec i%%10 = %02x" % (i, base, base10))
