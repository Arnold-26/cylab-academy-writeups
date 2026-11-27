#!/bin/bash
cd /tmp
cp ./_z_bizz_gen2.py .
python3 _z_bizz_gen2.py
grep -E '^[0-9]+$' /tmp/trace2.txt > /tmp/obs_n.txt
echo "observed plays: $(wc -l < /tmp/obs_n.txt)  expected rounds: $(wc -l < /tmp/bizz_rounds.txt)"
python3 - <<'PY'
obs=[int(x) for x in open('/tmp/obs_n.txt')]
exp=[int(x) for x in open('/tmp/bizz_rounds.txt')]
n=min(len(obs),len(exp))
bad=None
for i in range(n):
    if obs[i]!=exp[i]:
        bad=i; break
print("first divergence at index", bad)
if bad is None:
    print("prefix OK up to", n, "of", len(exp), "expected")
else:
    print("expected:", exp[max(0,bad-6):bad+8])
    print("observed:", obs[max(0,bad-6):bad+8])
PY
