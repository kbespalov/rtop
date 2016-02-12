import os
from metrics.domain import proc_io, proc_mem, proc_cpu


def read_io_stat(pid):
    with open(os.path.join('/proc', pid, 'io')) as stat:
        return proc_io(*[float(line.split(':')[1].strip()) for line in stat])


def read_cpu_stat(pid):
    with open(os.path.join('/proc', pid, 'stat')) as stat:
        raw_stat = stat.readline().split()
        stat = proc_cpu(pid=raw_stat[0],
                        name=raw_stat[1],
                        status=raw_stat[2],
                        utime=float(raw_stat[13]),
                        stime=float(raw_stat[14]),
                        threads=int(raw_stat[19]),
                        blkio_ticks=float(raw_stat[41]))
        return stat


def read_mem_stat(pid):
    with open(os.path.join('/proc', pid, 'statm')) as stat:
        return proc_mem(*[int(x) for x in stat.readline().split()[:-1]])


def read_uid(pid):
    with open(os.path.join('/proc', str(pid), 'status')) as stat:
        return stat.readlines()[7].split('	')[1]
