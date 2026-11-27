"""BFS slide path on the 495 map, pos=[row,col], east=+col, south=+row.
Constraints from the MAC oracle: command i is used at robot nonce 2i+1;
  d0 must be 'east'; d1 in {E,S}; d2 in {E,S,W}; d3+ any."""
MAP = [[0,0,0,0,1,0,0,0,0,1],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,1],
       [0,1,0,0,0,0,0,0,2,0],
       [0,0,0,0,0,0,0,0,1,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,1,0,0],
       [0,0,1,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0]]
N = 10
D = {"east": (0, 1), "south": (1, 0), "west": (0, -1), "north": (-1, 0)}
GOAL = (4, 8)


def slide(pos, d):
    dr, dc = D[d]
    r, c = pos
    while True:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < N and 0 <= nc < N):
            break
        if MAP[nr][nc] == 1:
            break
        r, c = nr, nc
    return (r, c)


def allowed(i):
    if i == 0: return ["east"]
    if i == 1: return ["east", "south"]
    if i == 2: return ["east", "south", "west"]
    return list(D)


# BFS over (pos, i)
from collections import deque
start = ((0, 0), 0)
prev = {start: None}
q = deque([start])
found = None
while q:
    pos, i = q.popleft()
    if pos == GOAL:
        found = (pos, i); break
    if i >= 12: continue
    for d in allowed(i):
        np = slide(pos, d)
        st = (np, i + 1)
        if st not in prev:
            prev[st] = ((pos, i), d)
            q.append(st)
if found:
    path = []
    st = found
    while prev[st] is not None:
        p, d = prev[st]
        path.append((d, p, st[0]))
        st = p
    path.reverse()
    print("PATH len", len(path))
    for k, (d, a, b) in enumerate(path):
        print(f"  cmd{k} nonce{2*k+1}: {d:5s} {a} -> {b}")
else:
    print("NO PATH")
# also print slide table for reference
print("\nfrom (0,0):", {d: slide((0,0), d) for d in D})
