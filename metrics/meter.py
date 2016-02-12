from collections import namedtuple
import os
import time
from metrics.domain import proc_snapshot, sys_snapshot, cpu_stat
import system_stat, process_stat


def create_procs_snapshot(pids=None):
    if not pids:
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    snapshots = dict.fromkeys(pids)
    for pid in snapshots:
        io = process_stat.read_io_stat(pid)
        cpu = process_stat.read_cpu_stat(pid)
        mem = process_stat.read_mem_stat(pid)
        uid = process_stat.read_uid(pid)
        snapshots[pid] = proc_snapshot(pid, cpu.name, uid, cpu.status, cpu.stime + cpu.utime, cpu.blkio_ticks,
                                       cpu.threads, mem.resident, io.write_bytes, io.read_bytes)
    return snapshots


def procs_snapshot_diff(snap_a, snap_b):
    pids = set(snap_a.keys()) & set(snap_b.keys())
    result = dict.fromkeys(pids)
    for pid in pids:
        a, b = snap_a[pid], snap_b[pid]
        used_ticks, wait_ticks = a.used_ticks - b.used_ticks, a.wait_ticks - b.wait_ticks
        wbytes, rbytes = a.wbytes - b.wbytes, a.rbytes - b.rbytes
        result[pid] = proc_snapshot(pid, b.name, b.uid, b.status, used_ticks, wait_ticks,
                                    b.threads, b.resident_mem, wbytes, rbytes)
    return result


def create_system_snapshot():
    cpu_stat = system_stat.read_cpu_stat()
    root_disk = system_stat.disk_usage("/")
    mem_stat = system_stat.read_mem_stat()
    return sys_snapshot(cpu_stat, mem_stat, root_disk)


def sys_snapshot_diff(snap_a, snap_b):
    diff = cpu_stat(*[(x - y) for x, y in zip(list(snap_a.cpu), list(snap_b.cpu))])
    return sys_snapshot(diff, snap_a.mem, snap_a.disk)


def get_pids():
    return [pid for pid in os.listdir('/proc') if pid.isdigit()]


class metric_producer:
    def __init__(self, delay=5):
        self.delay = delay
        self.last_sys_snapshot = None
        self.last_procs_snapshot = None

    def __iter__(self):
        return self

    def next(self):
        # building two a system and procs snapshots with delay
        timestamp = time.time()
        if self.last_sys_snapshot is None:
            system_snapshot_a = create_system_snapshot()
            procs_snapshot_a = create_procs_snapshot()
        else:
            system_snapshot_a = self.last_sys_snapshot
            procs_snapshot_a = self.last_procs_snapshot
        time.sleep(self.delay)
        self.last_sys_snapshot = create_system_snapshot()
        self.last_procs_snapshot = create_procs_snapshot()
        system = sys_snapshot_diff(self.last_sys_snapshot, system_snapshot_a)
        procs = procs_snapshot_diff(self.last_procs_snapshot, procs_snapshot_a)
        return dict(timestamp=timestamp, system=system, procs=procs)
