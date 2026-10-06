"""Windows job keeps ownership of Java descendants after their parent exits."""
import ctypes
from ctypes import wintypes as w
import os
import subprocess
import time


class Accounting(ctypes.Structure):
    _fields_ = [('user', ctypes.c_int64), ('kernel', ctypes.c_int64),
                ('period_user', ctypes.c_int64), ('period_kernel', ctypes.c_int64),
                ('faults', w.DWORD), ('total', w.DWORD), ('active', w.DWORD), ('terminated', w.DWORD)]


class WindowsGame:
    def __init__(self, command, **kwargs):
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        signatures = {
            'CreateJobObjectW': ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            'AssignProcessToJobObject': ([w.HANDLE, w.HANDLE], w.BOOL),
            'QueryInformationJobObject': ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p], w.BOOL),
            'TerminateJobObject': ([w.HANDLE, w.UINT], w.BOOL),
            'CloseHandle': ([w.HANDLE], w.BOOL),
        }
        for name, (args, result) in signatures.items():
            fn = getattr(self.api, name)
            fn.argtypes, fn.restype = args, result
        self.job = self.api.CreateJobObjectW(None, None)
        if not self.job:
            raise ctypes.WinError(ctypes.get_last_error())
        self.process = None
        try:
            # Attach before Java can create children; polling descendants can miss
            # an intermediate relauncher that exits between two observations.
            self.process = subprocess.Popen(command, creationflags=0x4, **kwargs)
            if not self.api.AssignProcessToJobObject(self.job, int(self.process._handle)):
                raise ctypes.WinError(ctypes.get_last_error())
            resume = ctypes.WinDLL('ntdll').NtResumeProcess
            resume.argtypes, resume.restype = [w.HANDLE], ctypes.c_long
            if resume(int(self.process._handle)) < 0:
                raise OSError('Не удалось возобновить запуск Minecraft')
        except BaseException:
            if self.process is not None:
                self.process.kill()
                self.process.wait()
            self.close()
            raise
        self.pid = self.process.pid

    def poll(self):
        info = Accounting()
        if not self.api.QueryInformationJobObject(self.job, 1, ctypes.byref(info), ctypes.sizeof(info), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return None if info.active else self.process.poll()

    def wait(self):
        while True:
            code = self.poll()
            if code is not None:
                return code
            time.sleep(0.1)

    def terminate_tree(self):
        if not self.api.TerminateJobObject(self.job, 1):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.job:
            self.api.CloseHandle(self.job)
            self.job = None


def launch_game(command, **kwargs):
    if os.name == 'nt':
        return WindowsGame(command, **kwargs)
    return subprocess.Popen(command, **kwargs)
