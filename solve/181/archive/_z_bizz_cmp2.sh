#!/bin/bash
cd /tmp
cp ./_z_bizz_t3.gdb .
python3 ./../_z_bizz_test.py > /dev/null 2>&1
timeout 120 gdb -q -batch -nx -x _z_bizz_t3.gdb ./_z_bizz > /tmp/trace3.txt 2>&1
sed -n 's/^PLAY \([0-9]*\)$/\1/p' /tmp/trace3.txt > /tmp/obs_n.txt
echo "observed plays: $(wc -l < /tmp/obs_n.txt)  expected rounds: $(wc -l < /tmp/bizz_rounds.txt)"
grep -c VULNREACHED /tmp/trace3.txt
python3 - <<'PY'
obs=[int(x) for x in open('/tmp/obs_n.txt')]
exp=[int(x) for x in open('/tmp/bizz_rounds.txt')]
n=min(len(obs),len(exp))
bad=None
for i in range(n):
    if obs[i]!=exp[i]:
        bad=i; break
if bad is None:
    print("prefix OK up to", n, "expected", len(exp), "observed", len(obs))
else:
    print("first divergence at", bad)
    print("expected:", exp[max(0,bad-6):bad+8])
    print("observed:", obs[max(0,bad-6):bad+8])
PY
