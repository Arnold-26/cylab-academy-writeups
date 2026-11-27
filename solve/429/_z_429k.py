import sys, ctypes, ctypes.wintypes as wt, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll")
EXE = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\win429\WinAntiDbg0x100.exe"
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


class PBI(ctypes.Structure):
    _fields_ = [("ExitStatus", ctypes.c_long), ("PebBaseAddress", ctypes.c_void_p),
                ("AffinityMask", ctypes.c_void_p), ("BasePriority", ctypes.c_long),
                ("UniqueProcessId", ctypes.c_void_p), ("Inherited", ctypes.c_void_p)]


si = STARTUPINFO()
si.cb = ctypes.sizeof(si)
pi = PI()
k32.CreateProcessW(EXE, None, None, None, False, DBG, None, None, ctypes.byref(si), ctypes.byref(pi))
ev = DE()
t0 = time.time()
done = False
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
            n = ctypes.c_size_t(0)
            k32.ReadProcessMemory(pi.hProcess, ctypes.c_void_p(ptr), buf, size, ctypes.byref(n))
            raw = buf.raw[:n.value]
            txt = raw.decode("utf-16le", "replace") if uni else raw.decode("latin-1", "replace")
            txt = txt.replace("\xab\xab", "").replace("\x00", "")
            if txt.strip():
                print("DEBUG:", txt[:300])
    elif ev.code == 1:
        ex = int.from_bytes(bytes(ev.u)[0:4], "little")
        if ex == 0x80000003:
            if not done:
                pbi = PBI()
                rl = ctypes.c_ulong(0)
                ntdll.NtQueryInformationProcess(wt.HANDLE(pi.hProcess), 0, ctypes.byref(pbi),
                                                ctypes.sizeof(pbi), ctypes.byref(rl))
                peb = pbi.PebBaseAddress
                got = ctypes.c_size_t(0)
                z = ctypes.create_string_buffer(b"\x00", 1)
                k32.WriteProcessMemory(pi.hProcess, ctypes.c_void_p(peb + 2), z, 1, ctypes.byref(got))
                z4 = ctypes.create_string_buffer(b"\x00\x00\x00\x00", 4)
                k32.WriteProcessMemory(pi.hProcess, ctypes.c_void_p(peb + 0xBC), z4, 4, ctypes.byref(got))
                print("PEB=0x%x : BeingDebugged + NtGlobalFlag effaces" % peb)
                done = True
        else:
            cont = 0x80010001
    elif ev.code == 5:
        k32.ContinueDebugEvent(ev.pid, ev.tid, cont)
        break
    k32.ContinueDebugEvent(ev.pid, ev.tid, cont)
k32.TerminateProcess(pi.hProcess, 0)
