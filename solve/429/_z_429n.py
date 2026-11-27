import sys, shutil, os, ctypes, ctypes.wintypes as wt, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"/tmp/cylab_eps\win429\WinAntiDbg0x100.exe"
DST = r"/tmp/cylab_eps\win429\patched.exe"
d = bytearray(open(SRC, "rb").read())
pat = b"\xff\x15\x14\x30\x40\x00"
new = b"\x31\xc0\x90\x90\x90\x90"
n = 0
i = 0
while True:
    i = d.find(pat, i)
    if i < 0:
        break
    d[i:i + 6] = new
    n += 1
    i += 6
print("patchs appliques:", n)
open(DST, "wb").write(bytes(d))
print("ecrit:", DST, os.path.getsize(DST))

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
DBG = 0x00000002


class STARTUPINFO(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("lpReserved", wt.LPWSTR), ("lpDesktop", wt.LPWSTR),
                ("lpTitle", wt.LPWSTR), ("dwX", wt.DWORD), ("dwY", wt.DWORD),
                ("dwXSize", wt.DWORD), ("dwYSize", wt.DWORD), ("dwXCountChars", wt.DWORD),
                ("dwYCountChars", wt.DWORD), ("dwFillAttribute", wt.DWORD), ("dwFlags", wt.DWORD),
                ("wShowWindow", wt.WORD), ("cbReserved2", wt.WORD), ("lpReserved2", ctypes.c_void_p),
                ("hStdInput", wt.HANDLE), ("hStdOutput", wt.HANDLE), ("hStdError", wt.HANDLE)]


class PI(ctypes.Structure):
    _fields_ = [("hProcess", wt.HANDLE), ("hThread", wt.HANDLE),
                ("dwProcessId", wt.DWORD), ("dwThreadId", wt.DWORD)]


class DE(ctypes.Structure):
    _fields_ = [("code", wt.DWORD), ("pid", wt.DWORD), ("tid", wt.DWORD),
                ("pad", wt.DWORD), ("u", ctypes.c_byte * 160)]


si = STARTUPINFO()
si.cb = ctypes.sizeof(si)
pi = PI()
k32.CreateProcessW(DST, None, None, None, False, DBG, None,
                   os.path.dirname(DST), ctypes.byref(si), ctypes.byref(pi))
ev = DE()
t0 = time.time()
while time.time() - t0 < 15:
    if not k32.WaitForDebugEvent(ctypes.byref(ev), 2000):
        continue
    cont = 0x00010002
    if ev.code == 8:
        data = bytes(ev.u)
        ptr = int.from_bytes(data[0:8], "little")
        uni = int.from_bytes(data[8:10], "little")
        ln = int.from_bytes(data[10:12], "little")
        if ptr and ln:
            size = ln * (2 if uni else 1) + 2
            buf = ctypes.create_string_buffer(size)
            got = ctypes.c_size_t(0)
            k32.ReadProcessMemory(pi.hProcess, ctypes.c_void_p(ptr), buf, size, ctypes.byref(got))
            raw = buf.raw[:got.value]
            txt = raw.decode("utf-16le", "replace") if uni else raw.decode("latin-1", "replace")
            txt = txt.replace("\xab\xab", "").replace("\x00", "")
            if txt.strip():
                print("DEBUG:", txt[:400])
    elif ev.code == 1:
        ex = int.from_bytes(bytes(ev.u)[0:4], "little")
        if ex != 0x80000003:
            cont = 0x80010001
    elif ev.code == 5:
        k32.ContinueDebugEvent(ev.pid, ev.tid, cont)
        break
    k32.ContinueDebugEvent(ev.pid, ev.tid, cont)
k32.TerminateProcess(pi.hProcess, 0)
