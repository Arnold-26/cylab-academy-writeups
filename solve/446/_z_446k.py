import sys, re, time, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import deque
CWD = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t446"


class P:
    def __init__(self, proc):
        self.p = proc
        self.buf = b""
    def recv(self, n):
        return self.p.stdout.read1(n)
    def sendall(self, b):
        self.p.stdin.write(b)
        self.p.stdin.flush()


def pump(pp, timeout=2.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            c = pp.recv(65536)
        except Exception:
            break
        if not c:
            break
        pp.buf += c


def parse_state(pp, timeout=3.0):
    pump(pp, timeout)
    txt = pp.buf.decode("utf-8", "replace")
    lines = txt.split("\n")
    grid = None
    for i, l in enumerate(lines):
        if "Lives left:" in l:
            g = lines[i + 1:i + 31]
            if len(g) >= 30 and all(len(x) >= 80 for x in g):
                grid = g
    lv = re.findall(r"Level: (\d+)", txt)
    lv = int(lv[-1]) if lv else 0
    pp.buf = b""
    return grid, lv, txt


def find(grid, ch):
    for y, row in enumerate(grid):
        x = row.find(ch)
        if x >= 0:
            return (y, x)
    return None


def bfs(grid, start, goal):
    q = deque([start])
    prev = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            path = []
            while prev[cur] is not None:
                p, d = prev[cur]
                path.append(d)
                cur = p
            return "".join(reversed(path))
        for d, (dy, dx) in (("s", (1, 0)), ("w", (-1, 0)), ("d", (0, 1)), ("a", (0, -1))):
            ny, nx = cur[0] + dy, cur[1] + dx
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != "#":
                if (ny, nx) not in prev:
                    prev[(ny, nx)] = (cur, d)
                    q.append((ny, nx))
    return None


EXPLOIT = "w" * 3 + "a" * 4 + "a" + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"

proc = subprocess.Popen(["./game"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=CWD)
pp = P(proc)
allout = ""
for level in range(1, 8):
    grid, lv, txt = parse_state(pp)
    if grid is None:
        print(f"niveau {level}: pas de grille, lv={lv}")
        allout += txt
        break
    end = find(grid, "X")
    path = bfs(grid, (1, 0), end)
    print(f"niveau {lv}: joueur={find(grid,'@')} sortie={end} chemin={len(path) if path else None}")
    seq = EXPLOIT + (path or "")
    pp.sendall(seq.encode())
    time.sleep(0.5)
    grid2, lv2, txt2 = parse_state(pp, 2.5)
    allout += txt2
    if lv2 > lv:
        print(f"  -> niveau {lv2} atteint")
        pp.sendall(b"")  # force refresh
        grid3, lv3, txt3 = parse_state(pp, 1.0)
        allout += txt3
    if "You win" in txt2 and lv2 == lv:
        print("  -> victoire finale ?")
    if "flag" in txt2.lower():
        break
proc.terminate()
print("=== extrait final ===")
print(allout[-400:])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", allout)
print("FLAG local:", m.group(0) if m else "non trouve")
