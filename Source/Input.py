

def pairFrom ( string ):
    
    numbers = string        \
        .replace('[','')    \
        .replace(']','')    \
        .strip()            \
        .split(',')
    
    numbers = map(float,numbers)
    
    return tuple(e for e in numbers)