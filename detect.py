#!/usr/libexec/platform-python

# Tracing all the openssl functions that called directly and indirectly
#
# One thing need to be figured out is how to locate the executives and libraries used by ebpf.bcc.
#

import time
import subprocess
from bcc import BPF


def bpf_text():
    """Return the function text that will be inserted into application space.
    :Return: a multiple line text"""
    text = """
#include <uapi/linux/ptrace.h>
#include <linux/ptrace.h>
//
// GET PID from executive itself.
// Found that in a lot of cases, it's hard to get the real pid.
// So just let the executive itself to report the PID, which requires
// the executive has a function with name 'getpid_' and return the pid
// of type u32.
//
// This function is also responsible for starting and stopping the
// probing.

BPF_HASH(probing_pid_table, u32, u32);
int getprobingpid(struct pt_regs *ctx){
    u32 _pid = (u32)PT_REGS_RC(ctx);
    u32 count = 0;
    u32* val = (u32*) probing_pid_table.lookup(&_pid);
    if (!val){
        probing_pid_table.update(&_pid, &count);
    } else {
        *val += 1;
    }
    // NOTE: Get the message with following command
    //   `sudo cat /sys/kernel/debug/tracing/trace_pipe`
    bpf_trace_printk("Global PID is %d\\n", _pid);
    return 0;
}

// Function probing info
struct funcinfo_t {
    u64 timestamp;
    u32 pid;
    u64 addr;
    char comm[TASK_COMM_LEN];
};
// TODO: Can this be replaced with new BPF type such as BPF_STACK?
BPF_HASH(funcinvoked, struct funcinfo_t, u64, 4096);

int dumpfuncname(struct pt_regs *ctx) {
    // NOTE: Any varable should be initialized, otherwize it panics.
    struct funcinfo_t info={0};
    u32 pid = bpf_get_current_pid_tgid()>>32;

    //u32 *val = probing_pid_table.lookup(&pid);
    //if (!val) {
    //    return 0;
    //}

    u64 addr = PT_REGS_IP(ctx);
    u64 timestamp = bpf_ktime_get_ns();
    info.timestamp = timestamp;
    info.pid = pid;
    info.addr = addr;
    bpf_get_current_comm(&info.comm, sizeof(info.comm));

    u64 zero=0;
    funcinvoked.update(&info, &zero);

    return 0;
};

//
// Add event to let bcc translate the function address to symbol
// before it exits.
//
// Demostrate a communication mechenism between injected code and
// bcc main loop.
struct process_exit_t {
    char comm[TASK_COMM_LEN];
    u32 pid;
};
//TODO: other than BPF_PERF_OUTPUT, is there any better way to
// communicate with python main thread?
BPF_PERF_OUTPUT(sleepfunc);

int detect_sleep(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid()>>32;
    struct process_exit_t et = {0};
    et.pid = pid;
    bpf_get_current_comm(&et.comm, sizeof(et.comm));
    sleepfunc.perf_submit(ctx, &et, sizeof(et));
    //bpf_trace_printk("PID is %d, comm is %s\\n", et.pid, et.comm);

    return 0;
}
"""
    return text


def main():
    bpf = BPF(text=bpf_text())
    qat_engine = '/usr/local/ssl/lib/engines-1.1/qatengine.so'
    #bpf.attach_uprobe(name="/lib64/libcrypto.so", sym_re='.*rsa.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name="/lib64/libcrypto.so", sym_re='.*RSA.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name="/lib64/libcrypto.so", sym_re='.*SSL.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name="/lib64/libcrypto.so", sym_re='.*ssl.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name="/lib64/libssl.so", sym_re='.*rsa.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name="/lib64/libssl.so", sym_re='.*RSA.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name="/lib64/libssl.so", sym_re='.*SSL.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name="/lib64/libssl.so", sym_re='.*ssl.*', fn_name='dumpfuncname')
    #bpf.attach_uprobe(name=qat_engine, sym_re='.*rsa.*', fn_name='dumpfuncname')
    bpf.attach_uprobe(name=qat_engine, sym_re='.*', fn_name='dumpfuncname')

    # The glibc symbols look tricky. Why it hasn't called a function named 'memset'
    # in libc.so, when we are called with 'memset'?
    # We cannot set probeing point at 'sym=memset', the actual libc.so symbole
    # for this is '__memset_avx2_unaligned_erms'
    print("Num open uprobe is ", bpf.num_open_uprobes())

    probing_tabel = bpf.get_table("probing_pid_table")
    looping = True

    print("Start polling for exiting condition ...")
    # Sleep 2 seconds to run payload if everything for probing is ready
    #cmd = "sleep 2 && {}".format(test_bin)
    #payload = subprocess.Popen(cmd, shell=True)

    while looping:
        try:
            bpf.perf_buffer_poll(timeout=100)
        except KeyboardInterrupt:
            looping = False
            probing_tabel.clear()
            pass
    # collecting funtion that called
    funcinvoked = bpf.get_table('funcinvoked')
    for k, v in funcinvoked.items():
        print(k.comm, bpf.sym(k.addr, k.pid, show_module=True, show_offset=True), "PID:", k.pid, k.addr)
    print("Waing for payload to reach the end ... ", end='')
    # payload.communicate()
    print("DONE")


if __name__ == '__main__':
    main()
