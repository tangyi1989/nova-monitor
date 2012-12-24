
def cpu_percent(start_cputime, end_cputime, start_time, end_time, ncpus):
    """
    Statistic cpu used percent by cputime used and real time used.
    cpu_percent = (end_cputime - start_cpu_time) / ( end_time - start_time )
    """
    delta_time = end_time - start_time
    delta_cputime = (end_cputime - start_cputime) / 1000
    if delta_cputime < 0 :
        delta_cputime = end_cputime
    
    return delta_cputime * 1.0 / (delta_time.microseconds * ncpus)

def io_bytes_rate(start_bytes, end_bytes, start_time, end_time):
    """
    Statistic io bytes rate.
    """

    delta_time = end_time - start_time
    delta_bytes = end_bytes - start_bytes
    if delta_bytes < 0 :
        delta_bytes = end_bytes
        
    return delta_bytes * 1000000 / delta_time.microseconds

def nic_traffic_info_read():
    """ Read nic traffic info and returns a dict of nic. """
    lines = open("/proc/net/dev", "r").readlines()
    
    columnLine = lines[1]
    _, receiveCols , transmitCols = columnLine.split("|")
    receiveCols = map(lambda a:"recv_"+a, receiveCols.split())
    transmitCols = map(lambda a:"trans_"+a, transmitCols.split())

    cols = receiveCols+transmitCols

    faces = {}
    for line in lines[2:]:
        if line.find(":") < 0: continue
        face, data = line.split(":")
        face = ''.join(face.split())
        faceData = dict(zip(cols, data.split()))
        faces[face] = faceData
        
    return faces
