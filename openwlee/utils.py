from datetime import datetime
import inspect

def methods_with_decorator(cls, decorator_name):
    method_names = []
    sourcelines = inspect.getsourcelines(cls)[0]
    
    for i,line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decorator_name: # leaving a bit out
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            method_names.append(name)
            
    return method_names

def cpu_percent(start_cputime, end_cputime, start_time, end_time, ncpus):
    delta_time = end_time - start_time
    delta_cputime = (end_cputime - start_cputime) / 1000
    if delta_cputime < 0 :
        delta_cputime = end_cputime
    
    return delta_cputime * 1.0 / (delta_time.microseconds * ncpus)

def io_bytes_speed(start_bytes, end_bytes, start_time, end_time):
    delta_time = end_time - start_time
    delta_bytes = end_bytes - start_bytes
    if delta_bytes < 0 :
        delta_bytes = end_bytes
        
    return delta_bytes * 1000000 / delta_time.microseconds

def utc_now():
    return datetime.utcnow()

def clear_screen():
    print "\033[2J"
