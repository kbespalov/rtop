# rtop
the python-based deamon for providing remote access to unix metrics by amqp

- config.py - describe auth credentials and remote host for mq server access
- /metrics - contains self-made metrics collector which can produce next values:
 - disk_stat:
    - 'total', 'used', 'free', 'percent'
 - mem_stat:
    - 'total', 'free', 'avaliable', 'buffers', 'cached'
 - cpu_stat:
    - 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest', 'guest_nice'
  - proc_snapshot (for each running proccess):
    - 'pid', 'name', 'uid', 'status', 'used_ticks', 'wait_ticks', 'threads', 'resident_mem', 'wbytes', 'rbytes'
