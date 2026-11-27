import sys, re, time, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import deque

BIN = "./game"
CWD = "/tmp/cylab_eps/t446"


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


proc = subprocess.Popen([BIN], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=CWD)
pp = P(proc)
grid = read_grid(pp)
print("grille:", grid is not None)
player = find(grid, "@")
goal = find(grid, "X")
print("joueur:", player, "sortie:", goal)
# exploit des vies puis retour en (0,0)
seq = "w" * 4 + "a" * 11 + "d" * 3 + "d" * 4
pp.sendall(seq.encode())
time.sleep(2.0)
proc.terminate()
# hmm : on relance proprement en envoyant tout d'un coup
proc2 = subprocess.Popen([BIN], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=CWD)
pp2 = P(proc2)
g2 = read_grid(pp2)
player2 = find(g2, "@")
goal2 = find(g2, "X")
path = bfs(g2, (0, 0), goal2)
print("chemin depuis (0,0):", len(path) if path else None)
full = "w" * 4 + "a" * 11 + "d" * 3 + "d" * 4 + (path or "")
print("sequence totale:", len(full))
pp2.sendall(full.encode())
time.sleep(3.0)
proc2.terminate()
proc3 = subprocess.run([BIN], input=full.encode() + b"\n", capture_output=True,
                       cwd=CWD, timeout=60)
out = proc3.stdout.decode("utf-8", "replace")
print("=== fin ===")
print(out[-400:])
print("You win:", "You win" in out)
