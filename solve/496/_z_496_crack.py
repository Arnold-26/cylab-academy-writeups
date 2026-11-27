import sys, json, time
sys.path.insert(0, '/tmp/smc')
from main import Untwister

bounds = json.load(open('/mnt/d/ctf-index/_z_496_bounds.json'))
print('n boundaries', len(bounds))
t0 = time.time()
ut = Untwister()
for b in bounds:
    s = bin(b)[2:].zfill(63)
    half1, half2 = s[:31], s[31:]
    ut.submit(half2)          # word0: full 32 bits
    ut.submit(half1 + '?')    # word1>>1 : top 31 bits known
print('submitted in %.1fs' % (time.time() - t0), flush=True)
r = ut.get_random()
print('solved in %.1fs' % (time.time() - t0), flush=True)
preds = [r.getrandbits(63) for _ in range(6)]
print('PRED', preds)
json.dump(preds, open('/mnt/d/ctf-index/_z_496_pred.json', 'w'))
