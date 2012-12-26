
# Used for looking up extensions of text
# to their 'multiplied' byte amount
BYTE_MULTIPLIERS = {
    '': 1,
    't': 1024 ** 4,
    'g': 1024 ** 3,
    'm': 1024 ** 2,
    'k': 1024,
}

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

def to_bytes(text, default=0):
    """Try to turn a string into a number of bytes. Looks at the last
    characters of the text to determine what conversion is needed to
    turn the input text into a byte number.
    
    Supports: B/b, K/k, M/m, G/g, T/t (or the same with b/B on the end)
    
    """
    # Take off everything not number 'like' (which should leave
    # only the byte 'identifier' left)
    mult_key_org = text.lstrip('-1234567890')
    mult_key = mult_key_org.lower()
    mult_key_len = len(mult_key)
    if mult_key.endswith("b"):
        mult_key = mult_key[0:-1]
    try:
        multiplier = BYTE_MULTIPLIERS[mult_key]
        if mult_key_len:
            # Empty cases shouldn't cause text[0:-0]
            text = text[0:-mult_key_len]
        return int(text) * multiplier
    except KeyError:
        msg = _('Unknown byte multiplier: %s') % mult_key_org
        raise TypeError(msg)
    except ValueError:
        return default

