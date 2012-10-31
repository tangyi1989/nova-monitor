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
