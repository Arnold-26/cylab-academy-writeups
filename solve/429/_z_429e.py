import sys, ctypes, ctypes.wintypes as wt, subprocess, os, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
EXE = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\win429\WinAntiDbg0x100.exe"
DEBUG_ONLY_THIS_PROCESS = 0x00000002
CREATE_NEW_CONSOLE = 0x00000010
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
EXCEPTION_DEBUG_EVENT = 1
CREATE_PROCESS_DEBUG_EVENT = 3
EXIT_PROCESS_DEBUG_EVENT = 5
OUTPUT_DEBUG_STRING_EVENT = 8


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
                ("dwThreadId", wt.DWORD), ("u", ctypes.c_byte * 160)]


si = STARTUPINFO()
si.cb = ctypes.sizeof(si)
pi = PROCESS_INFORMATION()
ok = k32.CreateProcessW(EXE, None, None, None, False,
                        DEBUG_ONLY_THIS_PROCESS, None, None,
                        ctypes.byref(si), ctypes.byref(pi))
if not ok:
    print("CreateProcess echoue:", ctypes.get_last_error())
    sys.exit(1)
print("lance sous debugger, pid", pi.dwProcessId)
ev = DEBUG_EVENT()
t0 = time.time()
while time.time() - t0 < 20:
    if not k32.WaitForDebugEvent(ctypes.byref(ev), 3000):
        continue
    code = ev.dwDebugEventCode
    cont = DBG_CONTINUE
    if code == OUTPUT_DEBUG_STRING_EVENT:
        # structure: ExceptionCode -> ici OutputDebugStringInfo {LPSTR lpDebugStringData; WORD fUnicode; WORD nDebugStringLength}
        data = bytes(ev.u)
        ptr = int.from_bytes(data[0:8], "little")
        unicode_flag = int.from_bytes(data[8:10], "little")
        length = int.from_bytes(data[10:12], "little")
        buf = ctypes.create_string_buffer(max(length * 2 + 2, 4))
        n = k32.ReadProcessMemory(pi.hProcess, ctypes.c_void_p(ptr), buf, length * 2 + 2, None)
        raw = buf.raw[:length * 2]
        if unicode_flag:
            txt = raw.decode("utf-16le", "replace")
        else:
            txt = raw[:length].decode("latin-1", "replace")
        print("DEBUG:", txt.rstrip("\x00"))
    elif code == EXCEPTION_DEBUG_EVENT:
        ex_code = int.from_bytes(bytes(ev.u)[0:4], "little", signed=False)
        if ex_code == 0x80000003:  # breakpoint initial
            cont = DBG_CONTINUE
        else:
            cont = DBG_EXCEPTION_NOT_HANDLED
    elif code == EXIT_PROCESS_DEBUG_EVENT:
        print("process termine")
        k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont)
        break
    k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, cont)
try:
    k32.TerminateProcess(pi.hProcess, 0)
except Exception:
    pass
