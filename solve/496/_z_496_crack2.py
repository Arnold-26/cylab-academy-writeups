import sys, json, time
from z3 import *
from random import Random
from itertools import count

SYMBOLIC_COUNTER = count()

def undo_right_shift_xor(y, shift):
    x = 0
    for i in range(31, -1, -1):
        bit = (y >> i) & 1
        if i + shift < 32:
            bit ^= (x >> (i + shift)) & 1
        x |= bit << i
    return x

def undo_left_shift_xor_mask(y, shift, mask):
    x = 0
    for i in range(32):
        bit = (y >> i) & 1
        if i - shift >= 0:
            bit ^= ((x >> (i - shift)) & 1) & ((mask >> i) & 1)
        x |= bit << i
    return x

def untemper(y):
    y = undo_right_shift_xor(y, 18)
    y = undo_left_shift_xor_mask(y, 15, 0xEFC60000)
    y = undo_left_shift_xor_mask(y, 7, 0x9D2C5680)
    y = undo_right_shift_xor(y, 11)
    return y

class U:
    def __init__(self):
        self.MT = [BitVec(f'MT_{i}', 32) for i in range(624)]
        self.index = 0
        self.solver = Solver()
        self.twists = 0

    def _symbolic_untamper(self, y):
        y1 = BitVec(f'y1_{next(SYMBOLIC_COUNTER)}', 32)
        y2 = BitVec(f'y2_{next(SYMBOLIC_COUNTER)}', 32)
        y3 = BitVec(f'y3_{next(SYMBOLIC_COUNTER)}', 32)
        y4 = BitVec(f'y4_{next(SYMBOLIC_COUNTER)}', 32)
        self.solver.add([
            y2 == y1 ^ (LShR(y1, 11)),
            y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
            y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
            y == y4 ^ (LShR(y4, 18)),
        ])
        return y1

    def _twist(self):
        MT = list(self.MT)
        for i in range(624):
            x = (MT[i] & 0x80000000) + (MT[(i + 1) % 624] & 0x7FFFFFFF)
            xA = LShR(x, 1)
            xB = If(x & 1 == 0, xA, xA ^ 0x9908B0DF)
            MT[i] = MT[(i + 397) % 624] ^ xB
        newMT = [BitVec(f'MT_{i}_{next(SYMBOLIC_COUNTER)}', 32) for i in range(624)]
        for i in range(624):
            self.solver.add(newMT[i] == MT[i])
        self.MT = newMT
        self.index = 0
        self.twists += 1

    def _prep(self):
        if self.index >= 624:
            self._twist()

    def submit_full(self, val):
        self._prep()
        self.solver.add(self.MT[self.index] == BitVecVal(untemper(val), 32))
        self.index += 1

    def submit_partial(self, guess):
        self._prep()
        name = next(SYMBOLIC_COUNTER)
        sg = BitVec(f'sg_{name}', 32)
        for i, bit in enumerate(guess.zfill(32)[::-1]):
            if bit != '?':
                self.solver.add(Extract(i, i, sg) == bit)
        y1 = self._symbolic_untamper(sg)
        self.solver.add(self.MT[self.index] == y1)
        self.index += 1

    def get_random(self):
        t = time.time()
        assert self.solver.check() == sat
        m = self.solver.model()
        print('solved in %.1fs' % (time.time() - t), flush=True)
        state = [m[self.MT[i]].as_long() if m[self.MT[i]] is not None else 0 for i in range(624)]
        r = Random()
        r.setstate((3, tuple(state + [self.index]), None))
        return r

# sanity check untemper
_r = Random(12345)
_raw = [_r.getrandbits(32) for _ in range(3)]
_st = list(_r.getstate()[1][:3])
assert [untemper(v) for v in _raw] == _st, 'untemper broken'
print('untemper ok')

bounds = json.load(open('./_z_496_bounds.json'))
print('n boundaries', len(bounds))
u = U()
t0 = time.time()
for b in bounds:
    s = bin(b)[2:].zfill(63)
    u.submit_full(int(s[31:], 2))
    u.submit_partial(s[:31] + '?')
print('submitted in %.1fs twists=%d index=%d' % (time.time() - t0, u.twists, u.index), flush=True)
r = u.get_random()
preds = [r.getrandbits(63) for _ in range(24)]
print('PRED', preds)
json.dump(preds, open('./_z_496_pred.json', 'w'))
