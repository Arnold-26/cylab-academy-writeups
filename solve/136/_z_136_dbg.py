import sys, re
exec(open('/mnt/d/ctf-index/_z_136_solve.py').read().split('# ------------------------------------------------------------------ client')[0])
log = open('/tmp/c136/log.txt').read()
m = re.search(r'flag ciphertext: ([0-9a-f]+)', log)
hx = m.group(1)
keys = re.findall(r'KEY\s+([0-9a-f ]+)', log)
print("hexlen", len(hx), "distinct keys", len(set(keys)))
kb = bytes.fromhex(keys[0].replace(' ', ''))
nb = len(hx) // 16
ct = int(hx, 16)
out = b''
for i in range(nb):
    b = (ct >> (64 * (nb - 1 - i))) & MASK64
    out += dec_block(b, kb).to_bytes(8, 'big')
print("decoded:", out)
# re-encrypt to check consistency
re_hex = ''.join('%016x' % enc_block(out[i:i+8], kb) for i in range(0, len(out), 8))
print("re-enc matches:", re_hex == hx)
# try every distinct key
for k in set(keys):
    kb2 = bytes.fromhex(k.replace(' ', ''))
    o = b''.join(dec_block((ct >> (64*(nb-1-i))) & MASK64, kb2).to_bytes(8,'big') for i in range(nb))
    print("key", k[:20], "->", o[:40])
