import sys, re, time, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import deque
CWD = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t446"


def read_grid(pp, timeout=2.5):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            c = pp.recv(65536)
        except Exception:
            break
        if not c:
            break
        pp.buf += c
        txt = pp.buf.decode("utf-8", "replace")
        if "Lives left:" in txt:
            lines = txt.split("\n")
            for i, l in enumerate(lines):
                if "Lives left:" in l:
                    grid = lines[i + 1:i + 31]
                    if len(grid) >= 30 and all(len(g) >= 80 for g in grid):
                        pp.buf = b""
                        return grid
    return None


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


class P:
    def __init__(self, proc):
        self.p = proc
        self.buf = b""
    def recv(self, n):
        return self.p.stdout.read1(n)
    def sendall(self, b):
        self.p.stdin.write(b)
        self.p.stdin.flush()
    def settimeout(self, t):
        pass


proc = subprocess.Popen(["./game"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=CWD)
pp = P(proc)
grid = read_grid(pp)
print("joueur:", find(grid, "@"), "sortie:", find(grid, "X"))
# exploit : w3 -> (1,4) ; a4 -> (1,0) ; a1 -> (1,-1) ; w1 -> (0,-1) ; a6 -> (0,-7) ; d3 -> (0,-4)
# ; d3 -> (0,-1) ; s1 -> (1,-1) ; d1 -> (1,0)
exploit = "w" * 3 + "a" * 4 + "a" * 1 + "w" * 1 + "a" * 6 + "d" * 3 + "d" * 3 + "s" * 1 + "d" * 1
path = bfs(grid, (1, 0), find(grid, "X"))
full = exploit + (path or "")
print("exploit:", len(exploit), "chemin:", len(path) if path else None, "total:", len(full))
p2 = subprocess.run(["./game"], input=full.encode() + b"\n", capture_output=True, cwd=CWD, timeout=90)
out = p2.stdout.decode("utf-8", "replace")
lives = re.findall(r"Lives left: (-?\d+)", out)
print("vies:", lives[:4], "...", lives[-2:] if lives else None)
print("You win:", "You win" in out)
print("fin:", out[-250:])
proc.terminate()
