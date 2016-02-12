from collections import namedtuple

proc_snapshot = namedtuple('proc_snapshot', ['pid',
                                             'name',
                                             'uid',
                                             'status',
                                             'used_ticks',
                                             'wait_ticks',
                                             'threads',
                                             'resident_mem',
                                             'wbytes',
                                             'rbytes'])

sys_snapshot = namedtuple('sys_snapshot', ['cpu',
                                           'mem',
                                           'disk'])

cpu_stat = namedtuple('cpu_stat', ['user',
                                   'nice',
                                   'system',
                                   'idle',
                                   'iowait',
                                   'irq',
                                   'softirq',
                                   'steal',
                                   'guest',
                                   'guest_nice'])

mem_stat = namedtuple('mem_stat', ['total',
                                   'free',
                                   'avaliable',
                                   'buffers',
                                   'cached'])

disk_stat = namedtuple('disk_stat', ['total',
                                     'used',
                                     'free',
                                     'percent'])

proc_io = namedtuple('proc_io', ['rchar',
                                 'wchar',
                                 'syscr',
                                 'syscw',
                                 'read_bytes',
                                 'write_bytes',
                                 'cancelled_write_bytes'])

proc_cpu = namedtuple('proc_cpu', ['pid',
                                   'name',
                                   'status',
                                   'utime',
                                   'stime',
                                   'threads',
                                   'blkio_ticks'])

proc_mem = namedtuple('proc_mem', ['total',
                                   'resident',
                                   'text',
                                   'lib',
                                   'data',
                                   'dt'])
