import os, sys
os.environ.setdefault('LOG', 'info')
import _z_sc55_pwn as E

gi = int(sys.argv[1]) if len(sys.argv) > 1 else 0
for attempt in range(8):
    try:
        E.p and E.p.close()
    except Exception:
        pass
    try:
        E.start('local')
        r = E.exploit(gadget_idx=gi)
    except Exception as ex:
        try:
            print("TAIL:", E.p.recvrepeat(1.5)[-400:])
        except Exception:
            pass
        print("EXC:", repr(ex))
        r = None
    if r:
        break
    print("retry", attempt)
st = None
try:
    st = E.p.poll(3)
except Exception as ex:
    print("POLLERR:", ex)
print("STATUS:", st)   # negative == signal
