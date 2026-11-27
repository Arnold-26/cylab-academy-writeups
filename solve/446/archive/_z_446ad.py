import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from collections import deque
sys.path.insert(0, r".")
from cylab2 import CyLab

MOVES = {"s": (1, 0), "w": (-1, 0), "d": (0, 1), "a": (0, -1)}


def recv_until_grid(s, timeout=10.0):
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
        if "No more lives" in txt or "obstacle" in txt:
            return None, txt
    return None, buf.decode("utf-8", "replace")


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
        for d, (dy, dx) in MOVES.items():
            ny, nx = cur[0] + dy, cur[1] + dx
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != "#":
                if (ny, nx) not in prev:
                    prev[(ny, nx)] = (cur, d)
                    q.append((ny, nx))
    return None


def advance(pos, seq):
    p = list(pos)
    for ch in seq:
        dy, dx = MOVES[ch]
        p[0] += dy
        p[1] += dx
    return tuple(p)


cy = CyLab(delay=1.0)
cy.login()


def start_instance():
    cy.req("PUT", "/api/challenges/446/instance/?source=library")
    for _ in range(12):
        time.sleep(2)
        st, b = cy.req("GET", "/api/challenges/446/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        if d.get("status") == "RUNNING":
            m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
            if m:
                return m.group(1), int(m.group(2))
    return None, None


for attempt in range(6):
    host, port = start_instance()
    if not host:
        print("instance KO")
        continue
    try:
        s = socket.create_connection((host, port), timeout=30)
    except Exception as e:
        print("connexion KO:", type(e).__name__)
        continue
    grid, txt = recv_until_grid(s)
    pos = (4, 4)
    won = 0
    flag = None
    for level in range(6):
        if grid is None:
            break
        p1 = bfs(grid, pos, (1, 0))
        if p1 is None:
            break
        exploit = p1 + "a" + "w" + "a" * 6 + "d" * 3 + "d" * 3 + "s" + "d"
        p2 = bfs(grid, (1, 0), (29, 89))
        if p2 is None:
            break
        s.sendall((exploit + p2).encode())
        pos = advance((1, 0), p2)
        time.sleep(0.25)
        grid, txt = recv_until_grid(s)
        if "You win" in txt:
            won += 1
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            flag = m.group(0)
            break
        if "No more lives" in txt or "obstacle" in txt:
            break
    s.close()
    print(f"essai {attempt}: niveaux gagnes={won} flag={flag}")
    if flag:
        break
