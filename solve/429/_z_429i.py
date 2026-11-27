import sys, ctypes, ctypes.wintypes as wt, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll")
EXE = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\win429\WinAntiDbg0x100.exe"
DEBUG_ONLY_THIS_PROCESS = 0x00000002
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001


class STARTUPINFO(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("lpReserved", wt.LPWSTR), ("lpDesktop", wt.LPWSTR),
                ("lpTitle", wt.LPWSTR), ("dwX", wt.DWORD), ("dwY", wt.DWORD),
                ("dwXSize", wt.DWORD), ("dwYSize", wt.DWORD), ("dwXCountChars", wt.DWORD),
                ("dwYCountChars", wt.DWORD), ("dwFillAttribute", wt.DWORD), ("dwFlags", wt.DWORD),
                ("wShowWindow", wt.WORD), ("cbReserved2", wt.WORD), ("lpReserved2", ctypes.c_void_p),
                ("hStdInput", wt.HANDLE), ("hStdOutput", wt.HANDLE), ("hStdError", wt.HANDLE)]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [("hProcess", wt.HANDLE), ("hThread", wt.HANDLE),
                ("dwProcessId", wt.DWORD), ("dwThreadId", wt.DWORD)]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [("dwDebugEventCode", wt.DWORD), ("dwProcessId", wt.DWORD),
                ("dwThreadId", wt.DWORD), ("pad", wt.DWORD),
                ("u", ctypes.c_byte * 160)]


class PROCESS_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [("ExitStatus", ctypes.c_long), ("PebBaseAddress", ctypes.c_void_p),
                ("AffinityMask", ctypes.c_void_p), ("BasePriority", ctypes.c_long),
                ("UniqueProcessId", ctypes.c_void_p), ("InheritedFromUniqueProcessId", ctypes.c_void_p)]


def clear_peb(hProc):
    pbi = PROCESS_BASIC_INFORMATION()
    rl = ctypes.c_ulong(0)
    st = ntdll.NtQueryInformationProcess(wt.HANDLE(hProc), 0, ctypes.byref(pbi),
                                         ctypes.sizeof(pbi), ctypes.byref(rl))
    print("NtQueryInformationProcess status=0x%x PEB=0x%x" % (st & 0xffffffff, pbi.PebBaseAddress or 0))
    if not pbi.PebBaseAddress:
        return
    n = ctypes.c_size_t(0)
    zero = ctypes.create_string_buffer(b"\x00", 1)
    ok = k32.WriteProcessMemory(hProc, ctypes.c_void_p(pbi.PebBaseAddress + 2), zero, 1, ctypes.byref(n))
    print("WriteProcessMemory ->", ok, "err", ctypes.get_last_error())


si = STARTUPINFO()
si.cb = ctypes.sizeof(si)
pi = PROCESS_INFORMATION()
if not k32.CreateProcessW(EXE, None, None, None, False, DEBUG_ONLY_THIS_PROCESS, None, None,
                          ctypes.byref(si), ctypes.byref(pi)):
    print("echec", ctypes.get_last_error())
    sys.exit(1)
ev = DEBUG_EVENT()
t0 = time.time()
patched = False
while time.time() - t0 < 20:
    if not k32.WaitForDebugEvent(ctypes.byref(ev), 2000):
        continue
    code = ev.dwDebugEventCode
    cont = DBG_CONTINUE
    if code == 8:
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
                print("DEBUG:", txt[:400])
    elif code == 1:
        ex = int.from_bytes(bytes(ev.u)[0:4], "little", signed=False)
        if ex == 0x80000003:
            if not patched:
                clear_peb(pi.hProcess)
                patched = True
            cont = DBG_CONTINUE
        else:
            cont = DBG_EXCEPTION_NOT_HANDLED
    elif code == 5:
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont)
        break
    k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont)
k32.TerminateProcess(pi.hProcess, 0)
