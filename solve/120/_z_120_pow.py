import socket, sys, time, re, hashlib, os
import multiprocessing as mp
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = open(r"/mnt/d/ctf-index/_z_120url.txt").read().split()
PORT = int(PORT)
print("cible:", HOST, PORT)


def pow_worker(args):
    prefix, target, start, step = args
    i = start
    cnt = 0
    while True:
        if hashlib.md5(prefix + str(i).encode()).digest()[-3:] == target:
            return prefix + str(i).encode()
        i += step
        cnt += 1


def solve_pow(prefix, target_hex, nproc=8):
    prefix_b = prefix.encode()
    target = bytes.fromhex(target_hex)
    t0 = time.time()
    ctx = mp.get_context("fork")
    with ctx.Pool(nproc) as pool:
        for res in pool.imap_unordered(pow_worker,
                                       [(prefix_b, target, k, nproc) for k in range(nproc)],
                                       chunksize=1):
            print("  PoW trouve en %.1fs : %r" % (time.time() - t0, res), flush=True)
            pool.terminate()
            return res.decode()
    return None


s = socket.create_connection((HOST, PORT), timeout=60)
s.settimeout(30)
buf = b""
end = time.time() + 60
while b"hex digits: " not in buf and time.time() < end:
    d = s.recv(65536)
    if not d:
        break
    buf += d
head = buf.decode("latin-1")
print("banner:", repr(head[:250]))
m = re.search(r"starts with \"(\d{5})\".*?hex digits: ([0-9a-f]{6})", head, re.S)
print("match:", m.groups() if m else None)
t0 = time.time()
ans = solve_pow(m.group(1), m.group(2))
print("reponse PoW:", ans, "(%.1fs)" % (time.time() - t0), flush=True)
s.sendall(ans.encode() + b"\n")
buf = b""
end = time.time() + 3600
while b"Clue : " not in buf and time.time() < end:
    d = s.recv(65536)
    if not d:
        print("connexion fermee")
        break
    buf += d
txt = buf.decode("latin-1")
print("apres PoW:", txt[:600])
mn = re.search(r"Public Modulus :\s+(\d+)", txt)
me = re.search(r"Clue :\s+(\d+)", txt)
if mn and me:
    open("/mnt/d/ctf-index/_z_120_ne.txt", "w").write(mn.group(1) + "\n" + me.group(1) + "\n")
    print("n et e sauves ; n bits =", len(mn.group(1)))
s.close()
