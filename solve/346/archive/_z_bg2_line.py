#!/usr/bin/env python3
"""Remote probe sending complete lines (pty canonical mode) and reporting after each."""
import sys, re, time, socket

host, port = sys.argv[1], int(sys.argv[2])
lines = [l.encode() for l in sys.argv[3:]]
if not lines:
    lines = [b"l" + b"y" + b"d" * 47, b"w", b"w", b"w", b"w", b"w"]

s = socket.create_connection((host, port), timeout=15)
s.settimeout(1.2)
buf = bytearray()
t0 = time.time()
eof = False

def drain(t=2.5):
    global eof
    end = time.time() + t
    idle = time.time()
    while time.time() < end:
        try:
            d = s.recv(262144)
        except socket.timeout:
            if time.time() - idle > 1.2:
                return
            continue
        if not d:
            eof = True
            return
        buf.extend(d)
        idle = time.time()

drain(1.5)
print("banner maps=%d eof=%s" % (buf.count(b'Player position'), eof))
for i, ln in enumerate(lines, 1):
    if eof:
        print("already EOF before line %d" % i)
        break
    s.sendall(ln + b"\n")
    before = buf.count(b'Player position')
    drain(2.5)
    m = re.findall(rb'Player position: (-?\d+) (-?\d+)', bytes(buf))
    print("line %d %-20r newmaps=%d last=%s eof=%s len=%d" % (
        i, ln[:20], buf.count(b'Player position') - before, m[-1] if m else None, eof, len(buf)))
txt = bytes(buf).decode('latin1', 'replace')
print("TOTAL maps=%d eof=%s len=%d" % (txt.count('Player position'), eof, len(buf)))
print("FLAGS:", re.findall(r'[A-Za-z0-9_]{2,}\{[^}\r\n]{3,}\}', txt))
print("not found:", 'not found' in txt, "| You win:", 'You win!' in txt)
print("tail:", repr(txt[-400:]))
s.close()
