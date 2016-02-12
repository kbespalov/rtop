import os
from metrics.domain import cpu_stat, mem_stat, disk_stat


def read_cpu_stat():
    with open('/proc/stat') as stat:
        return cpu_stat(*[int(value) for value in stat.readline().split()[1:]])


def read_mem_stat():
    with open('/proc/meminfo') as stat:
        raw_data = [int(stat.readline().split(' ')[-2]) for i in xrange(5)]
        return mem_stat(*raw_data)

def disk_usage(path='/'):
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize) // (1024 * 1024 * 1024)
    total = (st.f_blocks * st.f_frsize) // (1024 * 1024 * 1024)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize // (1024 * 1024 * 1024)
    percent = round((used * 100.0 / total), 1)
    return disk_stat(total, used, free, percent)
