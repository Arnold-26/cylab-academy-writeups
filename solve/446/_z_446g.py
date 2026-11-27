import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST, PORT = None, None
import subprocess


def read_state(s, timeout=3.0):
    """lit jusqu'a la fin de la carte, renvoie (lignes de map, position, texte)"""
    s.settimeout(timeout)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            c = s.recv(65536)
            if not c:
                break
            buf += c
            txt = buf.decode("utf-8", "replace")
            if "Lives left:" in txt:
                lines = txt.split("\n")
                for i, l in enumerate(lines):
                    if "Lives left:" in l:
                        grid = lines[i + 1:i + 31]
                        if len(grid) >= 30 and all(len(g) >= 80 for g in grid):
                            return grid, txt
        except socket.timeout:
            break
    return None, buf.decode("utf-8", "replace")


def find(grid, ch):
    for y, row in enumerate(grid):
        x = row.find(ch)
        if x >= 0:
            return (y, x)
    return None


def bfs(grid, start, goal, blocked="#"):
    from collections import deque
    q = deque([start])
    prev = {start: None}
    order = "wsad"
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
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if grid[ny][nx] in blocked:
                    continue
                nxt = (ny, nx)
                if nxt not in prev:
                    prev[nxt] = (cur, d)
                    q.append(nxt)
    return None


seq_static = "w" * 4 + "a" * 11 + "d" * 3
print("exploit vies:", len(seq_static), "coups")

# test local
p = subprocess.Popen(["./game"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     cwd="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t446")

class P:
    def __init__(self, proc):
        self.p = proc
    def recv(self, n):
        return self.p.stdout.read1(n)
    def sendall(self, b):
        self.p.stdin.write(b)
        self.p.stdin.flush()
    def settimeout(self, t):
        pass

pp = P(p)
grid, txt = read_state(pp, 3.0)
print("grille lue:", grid is not None)
if grid:
    print("joueur:", find(grid, "@"), "sortie:", find(grid, "X"))
    col0 = [grid[y][0] for y in range(5)]
    print("colonne 0 lignes 0-4:", col0)
    path = bfs(grid, find(grid, "@"), find(grid, "X"))
    print("chemin BFS long:", len(path) if path else None)
p.kill()
