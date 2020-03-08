from syscall_table import SYSCALL_TABLE
import ctypes
import os, sys

class user_regs_struct(ctypes.Structure):
    """
    ptraceで使用
    引数の型がC言語に準拠のため
    orig_rax    システムコール番号
    rax         前回のシステムコールの戻り値
    rdi         システムコールの第1引数
    rsi         システムコールの第2引数
    rdx         システムコールの第3引数
    """
    _fields_ = [
        ('r15', ctypes.c_ulonglong),
        ('r14', ctypes.c_ulonglong),
        ('r13', ctypes.c_ulonglong),
        ('r12', ctypes.c_ulonglong),
        ('rbp', ctypes.c_ulonglong),
        ('rbx', ctypes.c_ulonglong),
        ('r11', ctypes.c_ulonglong),
        ('r10', ctypes.c_ulonglong),
        ('r9', ctypes.c_ulonglong),
        ('r8', ctypes.c_ulonglong),
        ('rax', ctypes.c_ulonglong),
        ('rcx', ctypes.c_ulonglong),
        ('rdx', ctypes.c_ulonglong),
        ('rsi', ctypes.c_ulonglong),
        ('rdi', ctypes.c_ulonglong),
        ('orig_rax', ctypes.c_ulonglong),
        ('rip', ctypes.c_ulonglong),
        ('cs', ctypes.c_ulonglong),
        ('eflags', ctypes.c_ulonglong),
        ('rsp', ctypes.c_ulonglong),
        ('ss', ctypes.c_ulonglong),
        ('fs_base', ctypes.c_ulonglong),
        ('gs_base', ctypes.c_ulonglong),
        ('ds', ctypes.c_ulonglong),
        ('es', ctypes.c_ulonglong),
        ('fs', ctypes.c_ulonglong),
        ('gs', ctypes.c_ulonglong),
    ]

# /usr/include/linux/ptrace.h
PTRACE_TRACEME = 0
PTRACE_GETREGS = 12
PTRACE_SYSCALL = 24

libc = ctypes.CDLL(None)
ptrace = libc.ptrace

def main():
    trace_file = sys.argv[1]
    child_pid = os.fork()       # 監視プロセス(親)と被監視プロセス(子)が並行して実行される

    if child_pid == 0:
        # 被監視プロセスが行う処理
        ptrace(PTRACE_TRACEME, 0, 0, 0)
        os.execl('/usr/bin/python3', 'python', 'tracee_file')
        # os.execl('/usr/local/bin/python3', 'python', 'tracee_file')
        # os.execl('/usr/bin/python', 'python', 'tracee_file')
    else:
        # 監視プロセスが行う処理
        while True:
            """
            被監視プロセスが何らかの状態変化まで待機
            被監視プロセスが終了した場合0
            そうでない場合はシステムコールによって停止している状態
            """
            pid, status = os.wait()

            if status != 0:
                regs = user_regs_struct()
                ptrace(PTRACE_GETREGS, pid, 0, ctypes.pointer(regs))

                dump(regs)

                ptrace(PTRACE_SYSCALL, pid, 0, 0)
            else:
                sys.exit(0)


def dump(regs):
    syscall = SYSCALL_TABLE[regs.orig_rax]
    print(syscall, end='')
    print('({}, {}, {})'.format(regs.rdi, regs.rsi, regs.rdx), end='')
    print(' = ' + str(regs.rax))


if __name__ == '__main__':
    main()