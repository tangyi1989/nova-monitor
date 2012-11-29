
"""
Statistic cpu used percent by cputime used and real time used.
cpu_percent = (end_cputime - start_cpu_time) / ( end_time - start_time )
"""
def cpu_percent(start_cputime, end_cputime, start_time, end_time, ncpus):
    delta_time = end_time - start_time
    delta_cputime = (end_cputime - start_cputime) / 1000
    if delta_cputime < 0 :
        delta_cputime = end_cputime
    
    return delta_cputime * 1.0 / (delta_time.microseconds * ncpus)

"""
Statistic io bytes rate.
"""
def io_bytes_rate(start_bytes, end_bytes, start_time, end_time):
    delta_time = end_time - start_time
    delta_bytes = end_bytes - start_bytes
    if delta_bytes < 0 :
        delta_bytes = end_bytes
        
    return delta_bytes * 1000000 / delta_time.microseconds
