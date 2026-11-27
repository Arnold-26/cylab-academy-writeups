MAP = [[0,0,0,0,1,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,1],[0,1,0,0,0,0,0,0,2,0],[0,0,0,0,0,0,0,0,1,0],
       [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
N=10; D={"east":(0,1),"south":(1,0),"west":(0,-1),"north":(-1,0)}
CYC=["east","south","west","north"]; GOAL=(4,8)
def slide(p,d):
    dr,dc=D[d]; r,c=p
    while True:
        nr,nc=r+dr,c+dc
        if not(0<=nr<N and 0<=nc<N) or MAP[nr][nc]==1: break
        r,c=nr,nc
    return (r,c)
def avail(i, extras):
    return [CYC[i%4]] + [d for (dd,n) in extras if n==2*i+1 for d in [dd]]
from collections import deque
def bfs(extras, maxcmd=12):
    st=((0,0),0); prev={st:None}; q=deque([st])
    while q:
        pos,i=q.popleft()
        if pos==GOAL:
            path=[]; s=(pos,i)
            while prev[s] is not None:
                p,d=prev[s]; path.append((d,p,s[0])); s=p
            return path[::-1]
        if i>=maxcmd: continue
        for d in avail(i,extras):
            np=slide(pos,d); ns=(np,i+1)
            if ns not in prev:
                prev[ns]=((pos,i),d); q.append(ns)
    return None
for name,extras in [("pass2 only (east n<=13)",[("east",1),("east",3),("east",5),("east",7),("east",9),("east",11),("east",13)]),
                    ("pass2 long (east all odd)",[("east",n) for n in range(1,41,2)]),
                    ("pass2 long + pass3",[("east",n) for n in range(1,41,2)]+[("west",9)])]:
    p=bfs(extras)
    print(name, "->", None if not p else [(d,a,b) for d,a,b in p])
