import sys, os, re, time, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import deque
CWD = "/tmp/cylab_eps/t446"

proc = subprocess.Popen(["./game"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=CWD)
fd = proc.stdout.fileno()
os.set_blocking(fd, False)


def read_avail(t=1.0):
    out = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = os.read(fd, 65536)
        except BlockingIOError:
            time.sleep(0.02)
            continue
        except Exception:
            break
        if not c:
            break
        out += c
    return out


def parse(txt):
    lines = txt.split("\n")
    grid = None
    for i, l in enumerate(lines):
        if "Lives left:" in l:
            g = lines[i + 1:i + 31]
            if len(g) >= 30 and all(len(x) >= 80 for x in g):
                grid = g
    lv = re.findall(r"Level: (\d+)", txt)
    return grid, int(lv[-1]) if lv else 0


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


EXPLOIT = "w" * 3 + "a" * 5 + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
allout = ""
buf = b""
for level in range(1, 12):
    t0 = time.time()
    grid = None
    lv = 0
    while time.time() - t0 < 6:
        buf += read_avail(0.3)
        txt = buf.decode("utf-8", "replace")
        g, lvn = parse(txt)
        if g:
            grid, lv = g, lvn
            buf = b""
            break
    if grid is None:
        print(f"niveau {level}: pas de grille")
        break
    end = find(grid, "X")
    path = bfs(grid, (1, 0), end)
    print(f"niveau {lv}: sortie={end} chemin={len(path) if path else None} exploit+{len(EXPLOIT)}")
    if path is None:
        break
    proc.stdin.write((EXPLOIT + path).encode())
    proc.stdin.flush()
    time.sleep(0.4)
    buf += read_avail(1.5)
    allout += buf.decode("utf-8", "replace")
    if "academy{" in allout or "picoCTF{" in allout:
        print("FLAG trouve pendant le niveau", lv)
        break
proc.terminate()
print("=== fin ===")
print(allout[-500:])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", allout)
print("FLAG local:", m.group(0) if m else "non trouve")
